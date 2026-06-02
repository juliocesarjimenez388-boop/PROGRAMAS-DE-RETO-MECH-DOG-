import Hiwonder
import time
from HW_MechDog import MechDog

mechdog = MechDog()

time.sleep(2)

# 1. Bajar el cuerpo como gato agachado
mechdog.action_run("go_prone")
time.sleep(3)

# 2. Levantar un poco el torso, pero mantener postura baja
mechdog.transform([0, 0, -3], [0, -5, 0], 2000)
time.sleep(2)

# 3. Movimiento de acecho: avanzar lento
for i in range(4):
    mechdog.move(10, 0)   # avance suave
    time.sleep(0.6)
    mechdog.move(0, 0)
    time.sleep(0.4)

# 4. Detenerse
mechdog.move(0, 0)
time.sleep(1)

# 5. Regresar a postura normal lentamente
mechdog.transform([0, 0, 3], [0, 0, 0], 3000)
time.sleep(2)

mechdog.action_run("stand_four_legs")
