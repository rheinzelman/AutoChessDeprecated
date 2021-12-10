#include "AccelStepper.h" 
// AccelStepper Setup
AccelStepper stepperX(1, 4, 3);   // 1 = Easy Driver interface NANO Pin 4 connected to STEP pin of Easy Driver NANO Pin 3 connected to DIR pin of Easy Driver
AccelStepper steppery(1, 5, 6);   // 1 = Easy Driver interface NANO Pin 5 connected to STEP pin of Easy Driver NANO Pin 2 connected to DIR pin of Easy Driver

#define xSwitch 12 // Pin 12 connected to Home Switch (MicroSwitch)
#define ySwitch 13 // Pin 13 connected to  (MicroSwitch)
#define Hall_sensor 22
long TravelX;
long Travely;
int  state;
int stateH;    
int  move_finished = 1;
char original_messg;
char final_messg; 
const int len = 15;
const String utf_messg[len] = {"x58","x59","x78","x79","x30","x31","x32","x33","x34","x35","x36","x37","x38","x39","x2D"};
const char converted_messg[len] = {'X','Y','x','y','0','1','2','3','4','5','6','7','8','9','-'};
long initial_homing  = -1;  
long initial_homingy =  1;
void setup() 
{
      pinMode(Hall_sensor, INPUT_PULLUP);
      Serial.begin(9600); 
      pinMode(xSwitch, INPUT_PULLUP);
      pinMode(ySwitch, INPUT_PULLUP);
        //set pins rx and tx for serial communication
      pinMode(0, INPUT);
      pinMode(1, OUTPUT);
      //pinMode(HallEffectA1,INPUT);
     //delay(2);
      stepperX.setMaxSpeed(1000.0);
      steppery.setMaxSpeed(1000.0);
      stepperX.setAcceleration(1000.0);
      steppery.setAcceleration(1000.0);
      Serial.println("Stepper is Homing . . . . . . . . . . . ");
      while (digitalRead(ySwitch)) 
      {    
          steppery.moveTo(initial_homingy); 
          stepperX.moveTo(initial_homing);
          initial_homingy--;
          initial_homing++;
          steppery.run();
          stepperX.run();
      }
      steppery.setCurrentPosition(0);  
      steppery.setMaxSpeed(1000.0);  
      stepperX.setMaxSpeed(1000.0);
      steppery.setAcceleration(1000.0);
      stepperX.setAcceleration(1000.0);
      initial_homing  =  1;
      initial_homingy = -1;
      while (!digitalRead(ySwitch)) 
      {
          steppery.moveTo(initial_homingy);  
          stepperX.moveTo(initial_homing);  
          steppery.run();
          stepperX.run();
          initial_homing--;
          initial_homingy++;         
      }
     
      steppery.setCurrentPosition(0);
      stepperX.setCurrentPosition(0);
      Serial.println("Found Y-Limit");
      initial_homing  = -1; 
      initial_homingy =  1;
      steppery.setMaxSpeed(1000.0);  
      stepperX.setMaxSpeed(1000.0);
      stepperX.setAcceleration(1000.0);
      steppery.setAcceleration(1000.0);
      while (digitalRead(xSwitch)) 
      { 
          steppery.moveTo(initial_homing); 
          stepperX.moveTo(initial_homing);
          initial_homing++;  
          steppery.run();
          stepperX.run();
      }
      steppery.setCurrentPosition(0);
      stepperX.setCurrentPosition(0);  
      steppery.setMaxSpeed(1000.0);  
      stepperX.setMaxSpeed(1000.0);
      stepperX.setAcceleration(1000.0);
      steppery.setAcceleration(1000.0);
      initial_homing = 5;     
      while (!digitalRead(xSwitch)) 
      { 
          steppery.moveTo(initial_homing);  
          stepperX.moveTo(initial_homing);  
          steppery.run();
          stepperX.run();
          initial_homing--;
      }
          Travely = -100;
          TravelX = -100;
          steppery.moveTo(Travely);  
          stepperX.moveTo(TravelX);
          while ((stepperX.distanceToGo() != 0)&&(steppery.distanceToGo() != 0)) 
          {
              stepperX.run();  // Move Stepper into positio
              steppery.run();
          }
      steppery.setCurrentPosition(0);
      stepperX.setCurrentPosition(0);
      Serial.println("Found X-Limit");
      steppery.setMaxSpeed(2000.0);      
      stepperX.setMaxSpeed(2000.0);      
      steppery.setAcceleration(2000.0);  
      stepperX.setAcceleration(2000.0);
      Serial.println("Enter A Position");
}
void loop() 
{
    while (Serial.available()>0)  
    {
      original_messg = Serial.read();
      for (int i = 0; i < len; i++) 
      {
        if(utf_messg[i] == original_messg)
          final_messg = converted_messg[i];  
      }      
        move_finished=0;
        switch(final_messg)
        {
          case 1:
          Travely = 100;
          TravelX = -100;
          break;
          //=====================================================================================================
          case 2:
          move_finished=0;
          //=====================================================================================================
          Travely = 300;
          TravelX = -300;
          break;
          //=====================================================================================================
          case 3:
          Travely = 500;
          TravelX = -500;
          break;
          //=====================================================================================================
          case 4:
          Travely = 700;
          TravelX = -700;
          break;
          //=====================================================================================================
          case 5:
          Travely = 900;
          TravelX = -900;
          break;
          //=====================================================================================================
          case 6:
          Travely = 1100;
          TravelX = -1100;
          break;
          //=====================================================================================================
          case 7:
          Travely = 1300;
          TravelX = -1300;
          break;
          //=====================================================================================================
          case 8:
          Travely = 1500;
          TravelX = -1500;
          break;
          //=====================================================================================================
          case 9:
          Travely = -100;
          TravelX = -100;
          break;
          //=====================================================================================================
          case 10:
          //=====================================================================================================
          Travely = -300;
          TravelX = -300;
          break;
           //=====================================================================================================
          case 11:
          //=====================================================================================================
          Travely = -500;
          TravelX = -500;
          break;
           //=====================================================================================================
          case 12:
          //=====================================================================================================
          Travely = -700;
          TravelX = -700;
          break;
           //=====================================================================================================
          case 13:
          //=====================================================================================================
          Travely = -900;
          TravelX = -900;
          break;
           //=====================================================================================================
          case 14:
          Travely = -1100;
          TravelX = -1100;
          break;
          //=====================================================================================================
          case 15:
          //=====================================================================================================
          Travely = -1300;
          TravelX = -1300;
          break;
          //=====================================================================================================
          case 16:
          //=====================================================================================================
          Travely = -1500;
          TravelX = -1500;
          break;
         //=====================================================================================================
          case 17:
          Travely = -1880;
          TravelX = -1500;
          //=====================================================================================================
          steppery.moveTo(0);  
          stepperX.moveTo(0);
          //=====================================================================================================
         break;
        }
          //=====================================================================================================
          steppery.moveTo(Travely);  
          stepperX.moveTo(TravelX);
          //=====================================================================================================
          while ((stepperX.distanceToGo() != 0)&&(steppery.distanceToGo() != 0)) 
          {
              stepperX.run();  // Move Stepper into positio
              steppery.run();
          }
          if ((move_finished == 0) && (stepperX.distanceToGo() == 0)) 
          {
              Serial.println("COMPLETED!");
              Serial.println("Enter A New Position");
              move_finished=1;  // Reset move variable
          }
          
          //delay(5000);
          //steppery.moveTo(0);  
          stepperX.moveTo(0);
          //=====================================================================================================
          while ((stepperX.distanceToGo() != 0)&&(steppery.distanceToGo() != 0)) 
          {
              stepperX.run();  // Move Stepper into positio
              steppery.run();
          }
          if ((move_finished == 0) && (stepperX.distanceToGo() == 0)) 
          {
              Serial.println("COMPLETED!");
              Serial.println("Enter A New Position");
              move_finished=1;  // Reset move variable
          }
    }
    
  
}
