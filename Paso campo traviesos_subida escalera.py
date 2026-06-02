import time
from HW_MechDog import MechDog

# =========================
# INICIALIZAR ROBOT
# =========================

mechdog = MechDog()

time.sleep(2)

# =========================
# FUNCION LEER SERVOS
# =========================

def leer_servos(etiqueta):

    print("================================")
    print(etiqueta)
    print("================================")

    for servo in range(1, 9):

        try:

            valor = mechdog.read_servo(servo)

            print("Servo", servo, "=", valor)

        except Exception as e:

            print("Servo", servo, "= ERROR:", e)

    print("================================")


# =========================
# LECTURA INICIAL
# =========================

leer_servos("VALORES INICIALES")

# =========================
# CONFIGURACION BASE
# =========================

# PARAMETRO 1
# VELOCIDAD / PERIODO
gait_speed = 100

# PARAMETRO 2
# LONGITUD DEL PASO
gait_stride = 1500

# PARAMETRO 3
# ALTURA DEL PASO
gait_height = 30

# ALTURA DEL CUERPO
body_height = 10

# VELOCIDAD DE AVANCE
move_speed = 30

# =========================
# POSTURA BASE
# =========================

print("Aplicando postura...")

mechdog.transform(
    [0, 0, body_height],
    [0, 0, 0],
    1000
)

time.sleep(1)

# =========================
# CONFIGURAR CAMINATA MODIFICADA
# =========================

print("Aplicando gait modificado...")

mechdog.set_gait_params(
    gait_speed,
    gait_stride,
    gait_height
)

time.sleep(1)

# =========================
# CAMINAR MODIFICADO
# =========================

print("Caminando con gait modificado...")

mechdog.move(move_speed, 0)

time.sleep(10)

# =========================
# DETENER
# =========================

print("Deteniendo...")

mechdog.move(0, 0)

time.sleep(2)

# =========================
# REGRESAR NORMAL
# =========================

print("Regresando postura normal...")

mechdog.action_run("stand_four_legs")

time.sleep(4)

# =========================
# RESETEAR GAIT NORMAL
# =========================

print("Restaurando gait normal aproximado...")

mechdog.set_gait_params(
    150,
    500,
    40
)

time.sleep(2)

# =========================
# LECTURA FINAL
# =========================

leer_servos("VALORES FINALES")

# =========================
# PROBAR CAMINATA NORMAL
# =========================

print("Probando caminata normal restaurada...")

mechdog.move(20, 0)

time.sleep(6)

print("Deteniendo caminata...")

mechdog.move(0, 0)

time.sleep(2)

print("FIN")


