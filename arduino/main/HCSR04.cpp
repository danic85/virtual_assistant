#include "Arduino.h"
#include "HCSR04.h"

HCSR04::HCSR04(int trig, int ech)
{
    _triggerPin = trig;
    _echoPin = ech;
    pinMode( _triggerPin, OUTPUT );
    pinMode( _echoPin, INPUT);

    digitalWrite(_triggerPin, LOW);
}
long HCSR04::doPing()
{
    long duration, inches;
    int value;

    digitalWrite(_triggerPin, LOW);
    delayMicroseconds(2);
    digitalWrite(_triggerPin, HIGH);
    delayMicroseconds(5);
    digitalWrite(_triggerPin, LOW);
    duration = pulseIn(_echoPin, HIGH);
    inches = microsecondsToInches(duration); 
    return inches;
}
boolean HCSR04::obstacleDetected()
{
    if (doPing() > MIN_DISTANCE) return false;
    return true;
}
long HCSR04::microsecondsToInches(long microseconds)
{
  // According to Parallax's datasheet for the PING))), there are
  // 73.746 microseconds per inch (i.e. sound travels at 1130 feet per
  // second).  This gives the distance travelled by the ping, outbound
  // and return, so we divide by 2 to get the distance of the obstacle.
  // See: http://www.parallax.com/dl/docs/prod/acc/28015-PING-v1.3.pdf
  return microseconds / 74 / 2;
}
