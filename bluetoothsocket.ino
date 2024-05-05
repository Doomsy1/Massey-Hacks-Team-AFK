#include "BluetoothSerial.h"
#include <ESP32Servo.h>

BluetoothSerial SerialBT;
const int LEFTMO = 0, RIGHTMO = 1, TURRETANG = 2, ARMANG = 3, GRIPPERPOS = 4;

// const int FLF = 2;
// const int FLB = 4;

// const int BLF = 27;
// const int BLB = 26;

// const int FRF = 25;
// const int FRB = 33;

// const int BRF = 32;
// const int BRB = 35;

const int RF = 32;
const int RB = 27;

const int LF = 4;
const int LB = 2;


const int gripperServoPin = 33;
Servo gripperServo;

const int armServoPin = 14;
Servo armServo;

const int turretServoPin = 12;
Servo turretServo;

void setup() {
  SerialBT.begin("AFK ESP");
  // Serial.println("ESP32 Bluetooth is ready!");

  ESP32PWM::allocateTimer(0);
  gripperServo.setPeriodHertz(50);
  gripperServo.attach(gripperServoPin, 500, 2400);

  ESP32PWM::allocateTimer(1);
  armServo.setPeriodHertz(50);
  armServo.attach(armServoPin, 500, 2400);

  ESP32PWM::allocateTimer(2);
  armServo.setPeriodHertz(50);
  turretServo.attach(turretServoPin, 500, 2400);

  Serial.begin(115200);
}

void loop() {
  if (SerialBT.available()) {
    String data = SerialBT.readStringUntil('\n');
    processControllerInput(data);
  }
  delay(15);
}

void processControllerInput(String data) {
  float datanums[5] = {};
  int count = 0;
  while (count < 5) {
    datanums[count] = data.substring(0, data.indexOf(',')).toFloat();
    data = data.substring(data.indexOf(',') + 1, data.length());
    count++;
  }

  // Serial.print(datanums[0]);
  // Serial.print(" ");
  // Serial.print(datanums[1]);
  // Serial.print(" ");
  // Serial.print(datanums[2]);
  // Serial.print(" ");
  // Serial.print(datanums[3]);
  // Serial.print(" ");
  // Serial.println(datanums[4]);

  updateTankDrive(datanums[LEFTMO], datanums[RIGHTMO]);
  updateTurret(datanums[TURRETANG]);
  updateArm(datanums[ARMANG]);
  updateGripper(datanums[GRIPPERPOS]);
}

void updateTankDrive(float leftmotors, float rightmotors) {
  // analogWrite(FLF, 0);
  // analogWrite(FLB, 0);
  // analogWrite(BLF, 0);
  // analogWrite(BLB, 0);

  // analogWrite(FRF, 0);
  // analogWrite(FRB, 0);
  // analogWrite(BRF, 0);
  // analogWrite(BRB, 0);
  analogWrite(RF, 0);
  analogWrite(RB, 0);
  analogWrite(LF, 0);
  analogWrite(LB, 0);

  if (leftmotors < 0) {
    analogWrite(LB, abs(leftmotors));
    // analogWrite(LB, abs(leftmotors));
  } else if (leftmotors > 0) {
    analogWrite(LF, leftmotors);
    // analogWrite(LF, leftmotors);
  }

  if (rightmotors < 0) {
    analogWrite(RB, abs(rightmotors));
    // analogWrite(RB, abs(rightmotors));
  } else if (rightmotors > 0) {
    analogWrite(RF, rightmotors);
    // analogWrite(RF, rightmotors);
  }
}

void updateTurret(float turretAngle) {
  turretServo.write(0);
  turretServo.write(turretAngle);
}

void updateArm(float armAngle) {
  armServo.write(0);
  armServo.write(armAngle);
  Serial.println(armAngle);
}

void updateGripper(float gripperAngle) {
  gripperServo.write(0);
  gripperServo.write(gripperAngle);
}