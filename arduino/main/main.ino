

#include "L298N.h"
#include "Braillespeak.h"
#include "HCSR04.h"
//#include "InfraRed.h"

// Initialise Modules
L298N motors;
Braillespeak speak;
HCSR04 distance1 = HCSR04(A3,A4);
HCSR04 distance2 = HCSR04(A1,A2);
//InfraRed ir;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  motors.doAction(DIRECTION_FORWARDS, MOTOR_SPEED_FULL);
}
void loop() {
  // Adjust course if moving forwards and getting close to something, regardless of input
  motors.autoDrive(distance1, distance2);

// Removed because it will not return consistant codes. It was working in isolation
//  int irDirection = ir.getDirection();
//  if (irDirection != motors.getLastAction() && irDirection != -1){
//    motors.doAction(irDirection, MOTOR_SPEED_FULL);
//  }
  if (Serial.available() > 0) {
    String serialString = Serial.readString();
    String response = motors.handleSerial(serialString);
    if (response != "") speak.doAction(response);
    else speak.doAction(serialString);
  }
}
