/*
 * ------------------------------
 *  Linckia version 6.3 & HV version 1.7
 * ------------------------------
 * Last modified:  20 July 2015
 * Group: RAL Space Autonomous Systems Group
 * Contact: Aron Kisdi aron.kisdi@stfc.ac.uk
 * Organisation: RAL Space, STFC
 * ------------------------------
 */

// Import the Arduino Servo library
#include <SoftwareServo.h>
#include <Metro.h>
#include <Wire.h>

////// Create a Servo object for each PWM servo out
////~~~~~~~~~~Wheels~~~~~~~~~~//
SoftwareServo servo1; //Digital pin 3
SoftwareServo servo2; //Digital pin 11
SoftwareServo servo3; //Digital pin 6
int motor1ph = 4; //motor 1 phase Digital pin 4
int motor1en = 9; //motor 1 enable Digital pin 9 PWM
int motor2ph = 12; //motor 2 phase Digital pin 12
int motor2en = 10; //motor 2 enable Digital pin 10 PWM
int motor3ph = 8; //motor 3 phase Digital pin 8
int motor3en = 5; //motor 3 enable Digital pin 5 PWM
int motor4ph = 7; //motor 4 phase Digital pin 7
int motor4en = 13; //motor 4 enable Digital pin 13 PWM

int routeren = 2; //Digital pin 2 for enabling 3.3V regulator

// Common servo setup values
int minPulse = 544;   // minimum servo position, us microseconds
int startPulse = 1472;  //startup positions (middle/stop), degrees
int maxPulse = 2400;  // maximum servo position, us microseconds

// User commands over serial
int command[6];                        // raw input from serial buffer, 6 bytes
char data[8] = {255,0,0,0,0,0,0,254};
int startbyte;                         // start byte, begin reading input
int stopbyte;                          // end of command

// Servos
int servo;                                                // target servo variable
int pos;                                                  // servo position
int servos[3] = {0,0,0};       //current postition of servos
int servotargets[3] = {0,0,0}; //target position of servos
int servomovtimes[3] = {0,0,0};                           //time remaining to get to target position
float servospeed;                                         //temporary value for servo speed calculation

//Motors
int motor;                         // target motor variable
int pwm;                           // motor speed pwm
int power;
int motordir;                      // motor direction
int motors[4] = {0,0,0,0};         //speed of motor pwm line
int motorsdir[4] = {0,0,0,0};      //direction of motor
int motortargets[4] = {0,0,0,0};   //target speed of motor
int motormovtimes[4] = {0,0,0,0};  //time remaining to get to target speed
float motorspeed;                  //temporary value of motor speed calucaltion

//Iterators and time
int time;                 //timed command value
int i;                    // iterator command error check
int j = 0;                // iterator (get feedback)
int k;                    // iterator move joint

//feedback
int feedback;             // reading from analog port
int feedback10;           // variable for storing first two digits of feedback
int feedback100;          // variable for storing 100s decimal places of feedback
int analogpin;            // variable for setting which analog pin to read

//Metro objects for schedueled tasks
int moveint = 50;
int mfeedon = 0;
int mfeedint = 1000;
Metro MMove = Metro(moveint);
Metro motorfeedback = Metro(mfeedint);

//USER DEFINED FUNCTIONS

void PinSetup(){
  
  servo1.attach(3); //attach servo 1 pwm to Digital pin 3
  servo2.attach(11); //attach servo 2 pwm to Digital pin 11
  servo3.attach(6); //attach servo 3 pwm to Digital pin 6
  
  servo1.setMinimumPulse(minPulse); //sets the minimum pulse duration 0 degrees in microseconds (default 544)
  servo1.setMaximumPulse(maxPulse); //sets the maximum pulse duration 180 degrees in microseconds (default 2400)
  servo2.setMinimumPulse(minPulse); //sets the minimum pulse duration 0 degrees in microseconds (default 544)
  servo2.setMaximumPulse(maxPulse); //sets the maximum pulse duration 180 degrees in microseconds (default 2400)
  servo3.setMinimumPulse(minPulse); //sets the minimum pulse duration 0 degrees in microseconds (default 544)
  servo3.setMaximumPulse(maxPulse); //sets the maximum pulse duration 180 degrees in microseconds (default 2400)
  
  pinMode(motor1ph,OUTPUT);
  pinMode(motor1en,OUTPUT);
  pinMode(motor2ph,OUTPUT);
  pinMode(motor2en,OUTPUT);
  pinMode(motor3ph,OUTPUT);
  pinMode(motor3en,OUTPUT);
  pinMode(motor4ph,OUTPUT);
  pinMode(motor4en,OUTPUT);
  pinMode(routeren,INPUT);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);
  pinMode(A4, INPUT);
  pinMode(A5, INPUT);
  digitalWrite(A0, LOW);
  digitalWrite(A1, LOW);
  digitalWrite(A2, LOW);
  digitalWrite(A3, LOW);
  digitalWrite(A4, LOW);
  digitalWrite(A5, LOW);
  //digitalWrite(routeren, HIGH);
}

void MoveServo(int servo, int pos){
  Return(113,servo,pos,0);
  switch (servo) {
    case 1:
      servo1.write(pos);       // move servo1 to 'pos'
      break;
    case 2:
      servo2.write(pos);       // move servo2 to 'pos'
      break;
    case 3:
      servo3.write(pos);       // move servo3 to 'pos'
      break;
  }
}

void MoveMotor(int motor, int motordir, int pwm){
  //Return(111,motor,motordir,pwm);
  switch (motor) {
    case 1:
      if (motordir == 0){
        digitalWrite(motor1ph,LOW);   //set motor direction
        analogWrite(motor1en,pwm);           //set motor speed
      }
      if (motordir == 1){
        digitalWrite(motor1ph,HIGH);   //set motor direction
        analogWrite(motor1en,pwm);           //set motor speed
      }
      //analogWrite(motor1en,pwm);           //set motor speed
      break;
    case 2:
      if (motordir == 0){
        digitalWrite(motor2ph,LOW);   //set motor direction
        analogWrite(motor2en,pwm);           //set motor speed
      }
      if (motordir == 1){
        digitalWrite(motor2ph,HIGH);   //set motor direction
        analogWrite(motor2en,pwm);           //set motor speed
      }
      //analogWrite(motor2en,pwm);           //set motor speed
      break;
    case 3:
      if (motordir == 0){
        digitalWrite(motor3ph,LOW);   //set motor direction
        analogWrite(motor3en,pwm);           //set motor speed
      }
      if (motordir == 1){
        digitalWrite(motor3ph,HIGH);   //set motor direction
        analogWrite(motor3en,pwm);           //set motor speed
      }
      //analogWrite(motor3en,pwm);           //set motor speed
      break;
    case 4:
      if (motordir == 0){
        digitalWrite(motor4ph,LOW);   //set motor direction
        analogWrite(motor4en,pwm);           //set motor speed
      }
      if (motordir == 1){
        digitalWrite(motor4ph,HIGH);   //set motor direction
        analogWrite(motor4en,pwm);           //set motor speed
      }
      //analogWrite(motor4en,pwm);           //set motor speed
      break;
  }
}
 
void ReadAnalog(int targetPin){
  feedback = analogRead(targetPin); 
  feedback100 = feedback/100;
  feedback10 = feedback-feedback100*100;
  //Return(1,targetPin,feedback100,feedback10);
  if (feedback100 < 100){
   if (feedback10 < 100){
     Return(1,targetPin,feedback100,feedback10);
   }
  } 
} 
     
void CommandReceived(int command[6]){
  // check each part of the command
      //Return(command[0],command[1],command[2],command[3]);
      if (command[0] > 5){
        //Error invalid command
        Return(103,command[0],0,0);
      } // End of if invalid command

      //MOTOR COMMAND
      if (command[0] == 1){ 
        motor = command[1]; // 1-4
        motordir = command[2]; //0 or 1
        if (motordir == 0){
          pwm = -command[3]; //-255 to 0
        }
        if (motordir == 1){
          pwm = command[3]; // 0 to 255
        }
        time = ((command[4])*1000)+((command[5])*10); //milliseconds ??? WARNING THIS CAN BE HIGHER THAN 32767!rollover?
        
        motorsdir[motor-1] = motordir;
        motortargets[motor-1] = pwm;
        motormovtimes[motor-1] = time;
        //Return(103,motor,motordir,pwm);
      } 
      //SERVO COMMAND
      if (command[0] == 2){
        servo = command[1]; // 1-3
        pos = command[2]; // 0-180
        time = ((command[4])*1000)+((command[5])*10); //milliseconds ??? WARNING THIS CAN BE HIGHER THAN 32767!rollover?
        
        servotargets[servo-1] = pos;
        servomovtimes[servo-1] = time;
      } 
      //SENSOR direct command
      if (command[0] == 3){
        analogpin = command[1];
        ReadAnalog(analogpin);
      } 
      
      // automatic sensor interval command
      if (command[0] == 4){
        //TODO Start stop readout
        if (command[1] == 1){ //command for changeg feedback interval
          mfeedon = command[2]; //turn it on if 1 turn it off if 0
          //command[3] not used
          mfeedint = (command[4]*100)+command[5];
          motorfeedback.interval(mfeedint);  
        }
      } 
      
      //ping
      if (command[0] == 5){
        Return(104,0,0,0);
      } // End of Handshake
      
      //restart router
      if (command[0] == 6){
        digitalWrite(routeren, LOW);
        delay(100);
        digitalWrite(routeren, HIGH);
      } // End of Handshake
}

void MoveActuators(){
  //Moves actuator by a calculated increment every 10 milliseconds
  SoftwareServo::refresh(); //sync servos
  if (MMove.check() == 1){
    //servos
    k = 0;
    for (k; k<3;k++){//cycle through pwm outputs
      if (servos[k] != servotargets[k]){//if servo is not at new command target
        if (servomovtimes[k] < moveint){//if command time is less than 100 milisecond
          servos[k] = servotargets[k];
          MoveServo(k+1,servos[k]); //move immediately
          servomovtimes[k] = 0;
        } //end of if time is less than moveint milisecond
        else{//else if time > moveint milisecond
          servospeed = ((float)(servotargets[k] - servos[k])*moveint)/servomovtimes[k]; //calculated servo speed pwmchange/100ms
          servos[k] = servos[k]+ (int) (servospeed); // update servo matrix
          MoveServo(k+1,servos[k]); // move servo at calculted speed for 10ms
          servomovtimes[k] = servomovtimes[k]-moveint;
        } // End of incremental move of servo
      } //End of if adjusment is required
    } //End of for loop for each sevo
   //motors
   k = 0;
   for (k; k<4;k++){//cycle through motor outputs
      //Return(k,motors[k],motortargets[k],motormovtimes[k]);
      //if (motordir[k] == 1){
      if (motors[k] != motortargets[k]){//if motor is not at new command target
        if (motormovtimes[k] < moveint){//if command time is less than 100 milisecond
          motors[k] = motortargets[k];
          power = abs(motors[k]);
          MoveMotor(k+1,motorsdir[k],power); // move motor immediatly
          motormovtimes[k] = 0;
          //Return(k,motorsdir[k],abs(motortargets[k]),power);
          //Return(1,motorsdir[0],abs(motortargets[0]),abs(motors[0]));
          //Return(2,motorsdir[1],abs(motortargets[1]),abs(motors[1]));
          //Return(3,motorsdir[2],abs(motortargets[2]),abs(motors[2]));
        } //end of if time is less than moveint milisecond
        else{//else if time > moveint milisecond
          motorspeed = ((float)(motortargets[k] - motors[k])*moveint)/motormovtimes[k]; //calculated motor speed pwmchange/100ms
          motors[k] = motors[k]+ (int) (motorspeed); // update motor matrix
          power = abs(motors[k]);
          if (motors[k] <0){
            MoveMotor(k+1,0,power);
          }
          else{
            MoveMotor(k+1,1,power); 
          }      
          //MoveMotor(k+1,motorsdir[k],power); // move motor at calculted speed for 10ms
          motormovtimes[k] = motormovtimes[k]-moveint;
        } // End of incremental move of servo
      } //End of if adjusment is required
    } //End of for loop for each sevo
  }
}

void CheckSensors(){
  if (motorfeedback.check() == 1) { //time to check motor feedback
    if(mfeedon == 1){ //if it is on 0 is off 1 is on
      ReadAnalog(j);
      j = j + 1;
      if(j==5){
        j = 0;
      }
    } //end of checking if it is on
  } //end of metro check
}

void Return(int ID, int value, int value1, int value2){
  Serial.write(255);
  Serial.write(ID);
  Serial.write(value);
  Serial.write(value1);
  Serial.write(value2);
  Serial.write(254);
}
  
//ARDUINO SETUP and LOOP functions

void setup() { 
   PinSetup();  //set up I/O
   // Open the serial connection, baud 9600 (max: 115200)
   Serial.begin(9600);
//   pinMode(ledPin, OUTPUT);
//   digitalWrite(ledPin, HIGH);
} 

void loop() 
{ 
  // Check serial input (min 8 bytes in buffer)
   if (Serial.available() > 7){
     // Read the first byte
     startbyte = Serial.read();
     // If it's really the startbyte (255) ...
     if (startbyte == 255){
       // Read command
       for (i=0;i<6;i++){
         command[i] = Serial.read();
       }
       stopbyte = Serial.read();
       if (stopbyte == 254){
         //Return(command[0],command[1],command[2],command[3]);
         CommandReceived(command);
       } //end of accept command
       else{
         //Error wrong Stopbyte
         Return(102,stopbyte,0,0);
         //Reject or accept command, debug ???
       } //end of stopbyte check
    } //end of accept startbyte
     else{
       //Error wrong Startbyte
       Return(101,startbyte,0,0);
     } //end of reject startbyte
  } //end if serial.available
  
   //Do scheduled tasks
   //move things   
   MoveActuators();
   //CheckSensors
   //CheckSensors();
   //SoftwareServo::refresh(); //sync servos
  
}
  
