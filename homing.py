#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
brain_inertial = Inertial()
motor_12 = Motor(Ports.PORT12, False)
motor_1 = Motor(Ports.PORT1, False)
motor_4 = Motor(Ports.PORT4, False)
controller = Controller()



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
speed = 100

# Geting redy to home:
# Slowly starting to move it toward the barriar
# also limmiting torque so it wont try to squeeze into the barrier
motor_4.set_velocity(5, PERCENT)
motor_4.spin(REVERSE)
motor_4.set_max_torque(3, PERCENT)

# while it is moving we constently check the current on the motor
# this alows us to detect a barrier when a rapid increase happens
while True:
    ampcurrent = motor_4.current(CurrentUnits.AMP)
    brain.screen.set_cursor(1, 1)
    brain.screen.print("homing", ampcurrent)
    if ampcurrent > 0.25:
        # Land Ahoy! We reached the barrier, time for a break
        break

# stoping the motor and telling it not to fight the barrier
motor_4.set_stopping(COAST)
motor_4.stop()
# giving it a moment to release tension, this increases the acuracy of homing
wait(300, MSEC)
# declairing that this is now officialy poition 0
motor_4.set_position(0, DEGREES)
# optional, now we can move it to your real home (if pos 0 is not your home)
motor_4.set_velocity(10, PERCENT)
motor_4.set_stopping(HOLD)
motor_4.set_max_torque(100, PERCENT)
motor_4.spin_to_position(40, DEGREES)

#   "Home Sweet Home!"  - Motor

# the following is an example program for a driving tank
while True:
    motor_12.set_velocity(50, PERCENT)
    motor_1.set_velocity(speed, PERCENT)
    motor_12.spin_for(REVERSE, controller.axisD.position(), DEGREES, wait=False)
    motor_1.spin_for(FORWARD, controller.axisA.position(), DEGREES, wait=False)
    if controller.buttonFDown.pressing():
        speed = speed + -0.1
    if controller.buttonFUp.pressing():
        speed = speed + 0.1
    
    speed = min(speed, 100)
    speed = max(speed, 0)

    current_cannon_pos = motor_4.position(DEGREES)
    
    if controller.buttonEUp.pressing() and current_cannon_pos < 180:
       motor_4.spin(FORWARD) 
    elif controller.buttonEDown.pressing():
        motor_4.spin(REVERSE)
    else:
        motor_4.stop()

    brain.screen.clear_row(1)
    brain.screen.set_cursor(1, 1)
    brain.screen.print(speed, current_cannon_pos)

    wait(20, MSEC)
