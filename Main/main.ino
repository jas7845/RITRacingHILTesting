#include <due_can.h>
#define  testID     0x0A
#define  Max_len    8
#define  testMsgH   0x00000070

#define  testMsgL   0x656E6973
enum States{
  Idle,
  Send,
  Log
};
//SND 007 0 or 1
States state = Idle;
int counter = 0;
int start = 0;
int timeend  = 0;
int randCounter = 0;

/*
* need to change the CAN, not sure what to
* Arduino Method in the Arduino IDE
*/
void setup() {
  // put your setup code here, to run once:
  Can0.begin(CAN_BPS_500K);
  Can1.begin(CAN_BPS_500K);
  Serial.begin(115200);
  Serial.setTimeout(2);
}

/*
* need to change the CAN, not sure what to
* Arduino Method in the Arduino IDE
*/
void loop() {
  // put your main code here, to run repeatedly:
  switch(state){
    case Log: logData();
    case Idle:;//Do nothing if Idling
  }
}

/** Method to handle messages coming through the serial
*
*/
void serialEvent(){
    String msg = Serial.readString();
    String prefix = msg.substring(0,3);
    if (prefix ==  "SET"){

    }
    else if (prefix == "CHK"){

    }
    else if (prefix == "LOG"){
        state = Log;
        logData();
    }
    else if (prefix == "IDL"){
        state = Idle;
    }


}

/* somehow send the data
*/
void sendData(uint32_t ID,   uint8_t  data[]){

}

void logData(){
    //in his it calls a readCAN message
}

// Need string to hex converter