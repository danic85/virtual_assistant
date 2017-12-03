#ifndef L298N_h
#define L298N_h

#include "Arduino.h"

// wired connections
#define L298N_B_IA 10 // D10 --> Motor B Input A --> MOTOR B +
#define L298N_B_IB 11 // D11 --> Motor B Input B --> MOTOR B -
#define L298N_A_IA 9 // D9 --> Motor A Input A --> MOTOR A +
#define L298N_A_IB 6 // D6 --> Motor A Input B --> MOTOR A -

// functional connections
#define MOTOR_R_FWD L298N_B_IA
#define MOTOR_R_REV L298N_B_IB
#define MOTOR_L_FWD L298N_A_IA
#define MOTOR_L_REV L298N_A_IB

#define MOTOR_DELAY 1000 // brief delay for abrupt motor changes
#define MOTOR_SPEED_FULL 255
#define MOTOR_SPEED_HALF 200
#define MOTOR_SPEED_SLOW 100

#define DIRECTION_STOP 0
#define DIRECTION_FORWARDS 1
#define DIRECTION_REVERSE 2
#define DIRECTION_LEFT 3
#define DIRECTION_RIGHT 4

class L298N
{
  public:
    L298N();
    String doAction(int direction, int speed);
    String adjustCourse(int direction);
    int getLastAction();
    void stop();
    void stop(bool wait);
  private:
    int _lastAction;
    int _lastSpeed;
};

#endif
