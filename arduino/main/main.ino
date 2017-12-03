#include "L298N.h"
#include "Braillespeak.h"
#include "HCSR04.h"
#include "InfraRed.h"

// Initialise Modules
L298N motors;
Braillespeak speak;
HCSR04 distance1 = HCSR04(A3,A4);
HCSR04 distance2 = HCSR04(A1,A2);
InfraRed ir;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  motors.doAction(DIRECTION_FORWARDS, MOTOR_SPEED_FULL);
}

void loop() {
  // Adjust course if moving forwards and getting close to something, regardless of input
  if (motors.getLastAction() == DIRECTION_FORWARDS)
  {
    if (distance1.obstacleDetected()) {
      String response = motors.adjustCourse(DIRECTION_RIGHT);
//      speak.doAction(response);
    }
    if (distance2.obstacleDetected()) {
      String response = motors.adjustCourse(DIRECTION_LEFT);
//      speak.doAction(response);
    }
  }

// Removed because it will not return consistant codes. It was working in isolation
//  int irDirection = ir.getDirection();
//  if (irDirection != motors.getLastAction() && irDirection != -1){
//    motors.doAction(irDirection, MOTOR_SPEED_FULL);
//  }
  // Send string commands via serial to control:
  // 'm' = motors
  // 'f/b/l/r/'  = direction
  // 's/m/f' = speed
  // e.g. mfs = motor forwards slow. ml or mlf = motor left fast
  if (Serial.available() > 0) {
      // read the incoming command:
      String serialString = Serial.readString();
      char serialCommand[serialString.length()+1];
      serialString.toCharArray(serialCommand, serialString.length()+1);

      Serial.print("I received: ");
      Serial.println(serialString);

      int action = DIRECTION_STOP;
      int speed = MOTOR_SPEED_FULL;
      if (serialCommand[0] == 'm') {
        switch(serialCommand[1]){
          case 'f':
            action = DIRECTION_FORWARDS;
            break;
          case 'b':
            action = DIRECTION_REVERSE;
            break;
          case 'l':
            action = DIRECTION_LEFT;
            break;
          case 'r':
            action = DIRECTION_RIGHT;
            break;
          default:
            break;
        }
        if(serialString.length() > 2) {
          // handle speed
          switch(serialCommand[2]){
            case 's':
              speed = MOTOR_SPEED_SLOW;
              break;
            case 'm':
              speed = MOTOR_SPEED_HALF;
              break;
            default:
              break;
          }
        }
        String response = motors.doAction(action, speed);
        speak.doAction(response);
      }
      
  }
}
