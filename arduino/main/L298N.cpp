#include "Arduino.h"
#include "L298N.h"

L298N::L298N()
{
    pinMode( MOTOR_L_FWD, OUTPUT );
    pinMode( MOTOR_L_REV, OUTPUT );
    pinMode( MOTOR_R_FWD, OUTPUT );
    pinMode( MOTOR_R_REV, OUTPUT );

    // Stop but don't add delay
    _lastAction = DIRECTION_STOP;
    _lastSpeed = MOTOR_SPEED_SLOW;
    stop(false);
}
String L298N::autoDrive(HCSR04 d1, HCSR04 d2)
{
  String response;
  if (_lastAction == DIRECTION_FORWARDS)
  {
    if (d1.obstacleDetected()) {
      response = adjustCourse(DIRECTION_RIGHT);
    }
    if (d2.obstacleDetected()) {
      response = adjustCourse(DIRECTION_LEFT);
    }
  }
  return response;
}
String L298N::handleSerial(String serialString)
{
  // Send string commands via serial to control:
  // 'm' = motors
  // 'f/b/l/r/'  = direction
  // 's/m/f' = speed
  // e.g. mfs = motor forwards slow. ml or mlf = motor left fast

  if (serialString.length() > 3) return ""; // Ignore serial strings not meant for motors

  // read the incoming command:
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
    return doAction(action, speed);

  }
  return "";
  
}
String L298N::doAction(int direction, int speed)
{
    Serial.print("Motors: ");
    Serial.println(direction);
    
    if (direction == _lastAction && speed == _lastSpeed) return "";

     // Stop drive if not already stopped
    if (_lastAction != DIRECTION_STOP) stop();

    // Set last action
    _lastAction = direction;
    _lastSpeed = speed;

    String response = "Stopping";

    switch(direction)
    {
        case DIRECTION_FORWARDS:
            response = "Forwards";
            analogWrite( MOTOR_L_FWD, speed );
            analogWrite( MOTOR_R_FWD, speed );
            break;
        case DIRECTION_REVERSE:
            response = "Reverse";
            analogWrite( MOTOR_L_REV, speed );
            analogWrite( MOTOR_R_REV, speed );
            break;
        case DIRECTION_LEFT:
            response = "Left";
            digitalWrite( MOTOR_L_REV, speed);
            analogWrite( MOTOR_R_FWD, speed);
            break;
        case DIRECTION_RIGHT:
            response = "Right";
            digitalWrite( MOTOR_L_FWD, speed);
            analogWrite( MOTOR_R_REV, speed);
            break;
        default:
            break;
    }
    Serial.println(response);
    return response;
}
int L298N::getLastAction()
{
  return _lastAction;
}
String L298N::adjustCourse(int direction)
{
  if (_lastAction != DIRECTION_FORWARDS) {
    return ""; // Ignore input
  }
  Serial.print("Last speed:");
  Serial.println(_lastSpeed);
  int actionToResume = _lastAction;
  doAction(direction, _lastSpeed);
  delay(1000);
  doAction(actionToResume, _lastSpeed);
  return "Turn";
}
void L298N::stop()
{
  stop(true);
}
void L298N::stop(bool wait)
{
    Serial.println("Stopping");
    
    digitalWrite( MOTOR_L_FWD, LOW );
    digitalWrite( MOTOR_L_REV, LOW );
    digitalWrite( MOTOR_R_FWD, LOW );
    digitalWrite( MOTOR_R_REV, LOW );

    if (wait) delay( MOTOR_DELAY );
}
