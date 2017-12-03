#ifndef HCSR04_h
#define HCSR04_h

#include "Arduino.h"

class HCSR04
{
  public:
    HCSR04(int trig, int ech);
    long doPing();
    long microsecondsToInches(long microseconds);
  private:
    int _triggerPin;
    int _echoPin;
};

#endif
