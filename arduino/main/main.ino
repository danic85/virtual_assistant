

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

// Encoder Test
int DL0 = 3, DL1 = 5, DR0 = 2, DR1 = 4; // Pins for Right and Left encoders. DL0 and DR0 must be Interrupts
int lStat0, lStat1, rStat0, rStat1;
int lpos = 0, rpos = 0;  // variables keeping count of the pulses on each side
String dir = "None";
unsigned long lastMovement = 0;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  pinMode(DL0, INPUT);
  pinMode(DL1, INPUT);
  pinMode(DR0, INPUT);
  pinMode(DR1, INPUT);
  attachInterrupt(1, intLeft, RISING);
  attachInterrupt(0, intRight, RISING); 
//  Serial.begin(115200);

}
void loop() {
 if (motors.getLastAction() != DIRECTION_STOP) {
  if(lastMovement != 0 && millis() - lastMovement > 500) {
    motors.doAction(DIRECTION_STOP, MOTOR_SPEED_FULL);
  }
 }
 else {
  lastMovement = 0;
 }
  
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

void intLeft()  // This interrupt routine runs if the left side encoder is triggered (DL0)
{
  lStat0 = digitalRead(DL0);
  lStat1 = digitalRead(DL1);
  if(lStat1 > 0) // use DL1 to determine which direction we're moving. HIGH = Forwards
    lpos++;
  else
    lpos--;
  dir = "Left";
  lastMovement = millis();
  Serial.print(dir);
  Serial.println(lpos);
}

void intRight()    // This interrupt routine runs if the right side encoder is triggered (DR0)
{
  rStat0 = digitalRead(DR0);
  rStat1 = digitalRead(DR1);
  if(rStat1 > 0) // use DR1 to determine which direction we're moving. HIGH = Backwards
    rpos--;
  else
    rpos++;
  dir = "Right";
  lastMovement = millis();
  Serial.print(dir);
  Serial.println(rpos);
}
