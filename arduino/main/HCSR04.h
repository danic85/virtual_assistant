#ifndef HCSR04_h
#define HCSR04_h

#include "Arduino.h"

#define MIN_DISTANCE 6

class HCSR04
{
  public:
    HCSR04(int trig, int ech);
    long doPing();
    boolean obstacleDetected();
    long microsecondsToInches(long microseconds);
  private:
    int _triggerPin;
    int _echoPin;
};

#endif
