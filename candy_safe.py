from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
brain_inertial = Inertial()
motor_11 = Motor(Ports.PORT11, False)
motor_12 = Motor(Ports.PORT12, False)
touchled_10 = Touchled(Ports.PORT10)

# generating and setting random seed
def initializeRandomSeed():
    wait(100, MSEC)
    xaxis = brain_inertial.acceleration(XAXIS) * 1000
    yaxis = brain_inertial.acceleration(YAXIS) * 1000
    zaxis = brain_inertial.acceleration(ZAXIS) * 1000
    systemTime = brain.timer.system() * 100
    urandom.seed(int(xaxis + yaxis + zaxis + systemTime)) 
    
# Initialize random seed 
initializeRandomSeed()

#endregion VEXcode Generated Robot Configuration
screen_precision = 0
is_open = True

motor_12.set_velocity(5, PERCENT) 
motor_12.spin(REVERSE)
while True:
    ampcurrent = motor_12.current(CurrentUnits.AMP)
    brain.screen.set_cursor(1, 1)
    brain.screen.print("homing", ampcurrent)
    if ampcurrent > 0.15:
        break
motor_12.stop()
motor_12.set_velocity(100, PERCENT) 
pos = 0
direction = 0
combo = []
while True:
    prev_direction = direction
    prev_pos = pos
    pos = -motor_11.position(DEGREES)
    delta = pos - prev_pos
    if delta > 0:
        direction = 1
    elif delta < 0:
        direction = 0
    number = pos % 360
    if prev_direction != direction:
       combo.append (int(number))
       combo = combo[-3:]
    if len(combo) == 3 and 57 < combo[0] < 77 and 285 < combo[1] < 305 and combo[2] < 20 and not is_open:
        touchled_10.set_color(Color.GREEN)
        motor_12.spin_for(REVERSE, 90, DEGREES)
        combo = []
        is_open = True
    if is_open and touchled_10.pressing():
        touchled_10.set_color(Color.RED)
        is_open = False
        motor_12.spin_for(FORWARD, 90, DEGREES)
    if is_open:
        touchled_10.set_color(Color.GREEN)
    else:
        touchled_10.set_color(Color.RED)
    brain.screen.set_cursor(1, 1)
    brain.screen.print(prev_pos, number, direction, precision=screen_precision)
    brain.screen.set_cursor(2, 1)
    brain.screen.print(combo, precision=screen_precision)
    wait(0.1, SECONDS)
    brain.screen.clear_row(1)
    brain.screen.clear_row(2)
    wait(20, MSEC)
