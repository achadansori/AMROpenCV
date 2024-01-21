#include <Servo.h> // menyertakan library servo ke dalam program 
Servo Servo1;
Servo Servo2;
Servo Servo3;
Servo Servo4;
Servo servoMotor;  // Buat objek dari kelas Servo
int pos1, pos2, pos3, pos4 = 0;   
         
void setup(){ 
  Servo1.attach(8);
  Servo2.attach(7);
  Servo3.attach(6);
  Servo4.attach(5);
  Servo1.write(pos1);
  Servo2.write(pos2);
  Servo3.write(pos3);
  Servo4.write(pos4);
} 

void loop(){
  for(pos4 = 00; pos4 < 30; pos4 += 1){
  Servo4.write(pos4); //prosedur penulisan data PWM ke motor servo
  delay(50); //waktu tunda 15 ms                 
 }
 for(pos2 = 00; pos2 < 80; pos2 += 1){
  Servo2.write(pos2); //prosedur penulisan data PWM ke motor servo
  delay(50); //waktu tunda 15 ms                 
 }
  for(pos3 = 00; pos3 < 40; pos3 += 1){
  Servo3.write(pos3); //prosedur penulisan data PWM ke motor servo
  delay(50); //waktu tunda 15 ms                 
 }
  for(pos4 = 30; pos4>=1; pos4-=1){                              
  Servo4.write(pos4);                 
  delay(50);                        
 }
  for(pos3 = 40; pos3>=1; pos3-=1){                              
  Servo3.write(pos3);                 
  delay(50);                        
 }
  for(pos2= 80; pos2>=1; pos2-=1){                              
  Servo2.write(pos2);                 
  delay(50);                        
 }
  for(pos1 = 00; pos1 < 180; pos1 += 1){
  Servo1.write(pos1); //prosedur penulisan data PWM ke motor servo
  delay(50); //waktu tunda 15 ms                 
 }


  for(pos3 = 00; pos3 < 20; pos3 += 1){
    Servo3.write(pos3); //prosedur penulisan data PWM ke motor servo
    delay(50); //waktu tunda 15 ms                 
 }
  for(pos2 = 00; pos2 < 40; pos2 += 1){
  Servo2.write(pos2); //prosedur penulisan data PWM ke motor servo
  delay(50); //waktu tunda 15 ms                 
 }
  for(pos4 = 00; pos4 < 30; pos4 += 1){
    Servo4.write(pos4); //prosedur penulisan data PWM ke motor servo
    delay(50); //waktu tunda 15 ms                 
 }
  for(pos2 = 40; pos2>=1; pos2-=1){                              
  Servo2.write(pos2);                 
  delay(50);                        
 }
  for(pos3 = 20; pos3>=1; pos3-=1){                              
    Servo3.write(pos3);                 
    delay(50);                        
 }
  for(pos4 = 30; pos4>=1; pos4-=1){                              
    Servo4.write(pos4);                 
    delay(50);                        
 }
   for(pos1 = 180; pos1>=1; pos1-=1){                              
  Servo1.write(pos1);                 
  delay(50);                        
 }

}