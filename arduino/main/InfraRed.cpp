/*
 * IRremote: IRrecvDemo - demonstrates receiving IR codes with IRrecv
 * An IR detector/demodulator must be connected to the input RECV_PIN.
 * Version 0.1 July, 2009
 * Copyright 2009 Ken Shirriff
 * 
 * https://github.com/z3t0/Arduino-IRremote
 * http://arcfn.com
 */


int RECV_PIN = 7;

#include "Arduino.h"
#include "InfraRed.h"
#include "L298N.h"
//#include <IRremote.h>

//Panasonic arrows
#define FWD 54
#define REV 53
#define LFT 55
#define RGT 56
#define STP 75

//IRrecv irrecv(RECV_PIN);

InfraRed::InfraRed()
{
  // In case the interrupt driver crashes on setup, give a clue
  // to the user what's going on.
  Serial.println("Enabling IRin");
//  irrecv.enableIRIn(); // Start the receiver
  Serial.println("Enabled IRin");
}

int InfraRed::getDirection() {
  int direction = -1;
//  decode_results results;
//  if (irrecv.decode(&results)) {
//    Serial.println(results.decode_type);
//    Serial.println(results.address);
//    Serial.println(results.value, HEX);
//    int decoded = results.value;
//    if (decoded > 800) decoded = decoded - 800;
//    switch(decoded)
//    {
//      case FWD:
//        direction = DIRECTION_FORWARDS;
//        break;
//      case REV:
//        direction = DIRECTION_REVERSE;
//        break;
//      case LFT:
//        direction = DIRECTION_LEFT;
//        break;
//      case RGT:
//        direction = DIRECTION_RIGHT;
//        break;
//      case STP:
//        direction = DIRECTION_STOP;
//        break;
//    }
//    irrecv.resume(); // Receive the next value
//  }
  
  return direction;
}
