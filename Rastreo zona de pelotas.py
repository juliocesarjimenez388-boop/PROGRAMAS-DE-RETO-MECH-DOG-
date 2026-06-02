import Hiwonder
import time
import Hiwonder_IIC
from HW_MechDog import MechDog

'''
  BUSCAR COLOR ROJO
  + LEDS
  + ACERCAMIENTO POR AREA
  + INCLINACION FRONTAL SUAVE
  + BAJAR BRAZO
  + SOLTAR PELOTA CON GRIPPER
  + RETROCESO FINAL
'''

RED = 1
GREEN = 2
BLUE = 3

# =========================
# INICIAR CAMARA Y SONAR
# =========================
iic2 = Hiwonder_IIC.IIC(2)
cam = Hiwonder_IIC.ESP32S3Cam(iic2)

i2c1 = Hiwonder_IIC.IIC(1)
i2csonar = Hiwonder_IIC.I2CSonar(i2c1)

# =========================
# INICIAR ROBOT
# =========================
mechdog = MechDog()

time.sleep(3)

# =========================
# CONFIGURACION
# =========================
COLOR_OBJETIVO = RED

VELOCIDAD_ADELANTE = 45
VELOCIDAD_ACERCAMIENTO = 20
VELOCIDAD_RETROCESO = -35

ANGULO_IZQUIERDA = 25
ANGULO_DERECHA = -25

AREA_ACERCAMIENTO = 7000
AREA_SOLTAR = 20000

# =========================
# SERVOS
# =========================
SERVO_BRAZO = 9
SERVO_GRIPPER = 10

BRAZO_ARRIBA = 500
BRAZO_ABAJO = 1000

GRIPPER_ABIERTO = 0
GRIPPER_CERRADO = 1000

# =========================
# LEDS
# =========================
def led_apagado():
    i2csonar.setRGB(0, 0, 0, 0)

def led_rojo():
    i2csonar.setRGB(0, 250, 0, 0)

# =========================
# INCLINARSE HACIA ENFRENTE
# =========================
def inclinar_frente():

    print("Inclinando robot lentamente...")

    for angulo in range(0, 21):

        mechdog.set_pose(
            [0, 0, 0],
            [0, angulo, 0],
            800
        )

        time.sleep(0.12)

# =========================
# REGRESAR POSTURA NORMAL
# =========================
def regresar_postura():

    print("Regresando postura lentamente...")

    for angulo in range(20, -1, -1):

        mechdog.set_pose(
            [0, 0, 0],
            [0, angulo, 0],
            800
        )

        time.sleep(0.18)

    print("Postura regresada suave")

# =========================
# MOVER BRAZO SUAVE
# =========================
def mover_brazo_suave(inicio, fin, duracion, pasos):

    for i in range(pasos + 1):

        t = i / pasos

        curva = 3 * (t ** 2) - 2 * (t ** 3)

        posicion = int(
            inicio +
            (fin - inicio) * curva
        )

        mechdog.set_servo(
            SERVO_BRAZO,
            posicion,
            120
        )

        time.sleep(duracion / pasos)

# =========================
# SOLTAR PELOTA
# =========================
def soltar_pelota():

    print("Zona roja cerca... soltando pelota...")

    mechdog.move(0, 0)

    led_rojo()

    time.sleep(0.5)

    # Inclinar robot hacia enfrente
    inclinar_frente()

    # Bajar brazo suavemente
    mover_brazo_suave(
        BRAZO_ARRIBA,
        BRAZO_ABAJO,
        6.0,
        120
    )

    time.sleep(0.5)

    # Abrir gripper para soltar la pelota
    print("Abriendo gripper para soltar pelota...")

    mechdog.set_servo(
        SERVO_GRIPPER,
        GRIPPER_ABIERTO,
        1500
    )

    time.sleep(1.5)

    # Subir brazo suavemente
    mover_brazo_suave(
        BRAZO_ABAJO,
        BRAZO_ARRIBA,
        4.0,
        120
    )

    time.sleep(0.8)

    # Regresar postura normal
    regresar_postura()

    print("Pelota soltada")

    # Retroceso final
    print("Retrocediendo...")

    mechdog.move(
        VELOCIDAD_RETROCESO,
        0
    )

    time.sleep(3)

    mechdog.move(0, 0)

# =========================
# POSICION INICIAL BRAZO
# =========================

# El robot inicia con el brazo arriba
mechdog.set_servo(
    SERVO_BRAZO,
    BRAZO_ARRIBA,
    1500
)

time.sleep(1)

# IMPORTANTE:
# Como ahora el robot va a dejar la pelota,
# se asume que inicia con la pelota agarrada
mechdog.set_servo(
    SERVO_GRIPPER,
    GRIPPER_CERRADO,
    1500
)

time.sleep(1)

# =========================
# EJECUCION PRINCIPAL
# =========================
print("================================")
print("BUSCANDO ZONA ROJA PARA SOLTAR")
print("================================")

while True:

    color = cam.read_color(COLOR_OBJETIVO)

    if color != None:

        led_rojo()

        x = color[0]
        y = color[1]
        w = color[2]
        h = color[3]

        centro_x = x + (w / 2)

        area = w * h

        print(
            "X:",
            centro_x,
            "AREA:",
            area
        )

        angle = 0

        # =========================
        # CORRECCION IZQUIERDA/DERECHA
        # =========================
        if centro_x < 60:

            angle = ANGULO_IZQUIERDA

        elif centro_x > 100:

            angle = ANGULO_DERECHA

        else:

            angle = 0

        # =========================
        # ZONA ROJA MUY CERCA
        # =========================
        if area > AREA_SOLTAR:

            print("ZONA ROJA MUY CERCA, SOLTANDO...")

            mechdog.move(0, 0)

            time.sleep(0.5)

            soltar_pelota()

            break

        # =========================
        # ACERCAMIENTO POR AREA
        # =========================
        else:

            if area > AREA_ACERCAMIENTO:

                print("ACERCAMIENTO FINAL LENTO...")

                mechdog.move(
                    VELOCIDAD_ACERCAMIENTO,
                    angle
                )

            else:

                print("AVANZANDO HACIA ZONA ROJA...")

                mechdog.move(
                    VELOCIDAD_ADELANTE,
                    angle
                )

    else:

        led_apagado()

        print("NO DETECTA ROJO...")

        mechdog.move(0, 0)

    time.sleep(0.1)

# =========================
# FINAL
# =========================
mechdog.move(0, 0)

led_apagado()

print("================================")
print("PROGRAMA TERMINADO")
print("================================")
