#include "Wire.h"
#include <MPU6050_light.h>
#include <Servo.h>

Servo Servo1;
Servo Servo2;
Servo Servo3;
Servo Servo4;
Servo servoMotor;  // Buat objek dari kelas Servo
int pos1, pos2, pos3, pos4 = 0;   

MPU6050 mpu(Wire);
unsigned long timer = 0;
int loopCount = 0;  // Variabel untuk melacak jumlah iterasi
// Motor A
int enA = 38;
int inA1 = 22;
int inA2 = 24;
// Motor B
int enB = 40;
int inB1 = 26;
int inB2 = 28;
// Motor C
int enC = 42;
int inC1 = 30;
int inC2 = 32;
// Motor D
int enD = 44;
int inD1 = 34;
int inD2 = 36;

int speedA;
int speedB;
int speedC;
int speedD;

void setup() {
  Servo1.attach(8);
  Servo2.attach(7);
  Servo3.attach(6);
  Servo4.attach(5);
  Servo1.write(pos1);
  Servo2.write(pos2);
  Servo3.write(pos3);
  Servo4.write(pos4);
  Serial.begin(9600);
  Wire.begin();
  byte status = mpu.begin();
	// Set all the motor control pins to outputs
	pinMode(enA, OUTPUT);
	pinMode(enB, OUTPUT);
  pinMode(enC, OUTPUT);
	pinMode(enD, OUTPUT);
	pinMode(inA1, OUTPUT);
	pinMode(inA2, OUTPUT);
	pinMode(inB1, OUTPUT);
	pinMode(inB2, OUTPUT);
  pinMode(inC1, OUTPUT);
	pinMode(inC2, OUTPUT);
	pinMode(inD1, OUTPUT);
	pinMode(inD2, OUTPUT);
	
	// Turn off motors - Initial state
	digitalWrite(inA1, LOW);
	digitalWrite(inA2, LOW);
	digitalWrite(inB1, LOW);
	digitalWrite(inB2, LOW);
  digitalWrite(inC1, LOW);
	digitalWrite(inC2, LOW);
	digitalWrite(inD1, LOW);
	digitalWrite(inD2, LOW);
}

void forward () {
	digitalWrite(inA1, HIGH);
	digitalWrite(inA2, LOW);
	digitalWrite(inB1, HIGH);
	digitalWrite(inB2, LOW);
  digitalWrite(inC1, HIGH);
	digitalWrite(inC2, LOW);
	digitalWrite(inD1, HIGH);
	digitalWrite(inD2, LOW);
}
void stop () {
	digitalWrite(inA1, LOW);
	digitalWrite(inA2, LOW);
	digitalWrite(inB1, LOW);
	digitalWrite(inB2, LOW);
  digitalWrite(inC1, LOW);
	digitalWrite(inC2, LOW);
	digitalWrite(inD1, LOW);
	digitalWrite(inD2, LOW);
}

void arm () {
  for(pos4 = 00; pos4 < 30; pos4 += 1){
  Servo4.write(pos4); //prosedur penulisan data PWM ke motor servo
  delay(10); //waktu tunda 15 ms                 
 }
 for(pos2 = 00; pos2 < 90; pos2 += 1){
  Servo2.write(pos2); //prosedur penulisan data PWM ke motor servo
  delay(20); //waktu tunda 15 ms                 
 }
  for(pos3 = 00; pos3 < 50; pos3 += 1){
  Servo3.write(pos3); //prosedur penulisan data PWM ke motor servo
  delay(20); //waktu tunda 15 ms                 
 }
  for(pos4 = 30; pos4>=1; pos4-=1){                              
  Servo4.write(pos4);                 
  delay(10);                        
 }
  for(pos3 = 50; pos3>=1; pos3-=1){                              
  Servo3.write(pos3);                 
  delay(20);                        
 }
  for(pos2= 90; pos2>=1; pos2-=1){                              
  Servo2.write(pos2);                 
  delay(20);                        
 }
  for(pos1 = 00; pos1 < 180; pos1 += 1){
  Servo1.write(pos1); //prosedur penulisan data PWM ke motor servo
  delay(30); //waktu tunda 15 ms                 
 }


  for(pos3 = 00; pos3 < 20; pos3 += 1){
    Servo3.write(pos3); //prosedur penulisan data PWM ke motor servo
    delay(20); //waktu tunda 15 ms                 
 }
  for(pos2 = 00; pos2 < 40; pos2 += 1){
  Servo2.write(pos2); //prosedur penulisan data PWM ke motor servo
  delay(20); //waktu tunda 15 ms                 
 }
  for(pos4 = 00; pos4 < 30; pos4 += 1){
    Servo4.write(pos4); //prosedur penulisan data PWM ke motor servo
    delay(10); //waktu tunda 15 ms                 
 }
  for(pos2 = 40; pos2>=1; pos2-=1){                              
  Servo2.write(pos2);                 
  delay(20);                        
 }
  for(pos3 = 20; pos3>=1; pos3-=1){                              
    Servo3.write(pos3);                 
    delay(20);                        
 }
  for(pos4 = 30; pos4>=1; pos4-=1){                              
    Servo4.write(pos4);                 
    delay(10);                        
 }
   for(pos1 = 180; pos1>=1; pos1-=1){                              
  Servo1.write(pos1);                 
  delay(30);                        
 }
}

void loop() {
  mpu.update();
  
if (loopCount < 10) {
    forward();
    analogWrite(enA, speedA);
    analogWrite(enB, speedB);
    analogWrite(enC, speedC);
    analogWrite(enD, speedD);

    if (mpu.getAngleZ() > 0) {
      speedA = 170;
      speedB = 170;
      speedC = 0;
      speedD = 0;
    }

    if (mpu.getAngleZ() < 0) {
      speedA = 0;
      speedB = 0;
      speedC = 170;
      speedD = 170;
    }

    delay(10);
    loopCount++;
  } else {
    stop();
    arm();
  }
}

