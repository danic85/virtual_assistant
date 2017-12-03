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
  delay(500);
  doAction(actionToResume, _lastSpeed);
  return "Adjusted Course";
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
