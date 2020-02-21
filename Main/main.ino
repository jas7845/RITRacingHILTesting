#include <stdio.h>
//#include <due_can.h>
#define  testID     0x0A
#define  Max_len    8
#define  testMsgH   0x00000070

#define  testMsgL   0x656E6973
enum States{
  Idle,
  Send,
  Set,
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
  //printf("in loop main");
//  Can0.begin(CAN_BPS_500K);
//  Can1.begin(CAN_BPS_500K);
  
  Serial.begin(115200);
  Serial.println("setup");
  Serial.setTimeout(2);
  //serialEvent();
  delay(2000);
}

/**
* Logs the data by calling the readCAN method
*/
void logData(){
//keep the same
  //Continuously read data
//    readCAN();
    //delay(1);
}

/**
* Does something

void readCAN(){
//  Can0.watchFor();
  String msg = "";
  CAN_FRAME incoming;
//  if(Can0.available()>0){
//    Can0.read(incoming);
    //Serial.print(const_char(incoming.id));
    //Serial.print(String(incoming.id));
  }
}
*/
/**
* need to change the CAN, not sure what to
* Arduino Method in the Arduino IDE
*/
void loop() {
  // put your main code here, to run repeatedly:
  //printf("in loop main");
  //serialEvent();
  switch(state){
    case Log: logData();
    case Idle:;//Do nothing if Idling
  }
}


/**
* Sets a pin either high or low based on the data
*/
void setDataDigital(int id, int data){
    pinMode(id, OUTPUT);
    //Serial.println("in setDATA main");
    delay(500);
    Serial.print(data);
    Serial.print(".");
    if(data == 1){
        //Serial.println("HIGH");
        digitalWrite(id, HIGH);
        delay(2000);
    }
    else{
        //Serial.println("LOW");
        digitalWrite(id, LOW);
        delay(2000);
    }
}

/**
* Sets a pin either high or low based on the data
*/
void setDataAnalog(int id, int data){
    // values between 0 and 4095
//    analogWriteResolution(12);
    pinMode(id, OUTPUT);
    //Serial.println("in setDATA main");
    // values between 0 and 4095
    // when i put in 300 it consistently goes to .7 on reader thing
    // due is 3.3V, 12bit resolution, DAC0 == A0
    //Serial.println(data);
    //analogWrite(id, 0);
    if(data <= 4094){
      //Serial.println(data);
      analogWrite(id, data);
    }
    delay(1000);
}


/**
* Sets a pin either high or low based on the data
*/
int checkDataDigital(int id, int data){
    pinMode(id, OUTPUT);
    //Serial.println("in checkDATA main");
    int val = digitalRead(id);
    if((data == 1) and (val == HIGH)){
        Serial.println("HIGH");
        return 1;
        delay(2000);
    }
    else if ((data == 0) and (val == LOW)){
        return 0;
        delay(2000);
    }
    return val;
}

/**
* Sets a pin either high or low based on the data
*/
int checkDataAnalog(int id, int data){
    // change max resolution to 12 bits not 10
//    analogReadResolution(12);
    pinMode(id, OUTPUT);
    //Serial.println("in checkDATA main");
    int val = analogRead(id);
    return val;
    delay(200);
}

// keep the same
/**
* Sends data to a pin

void sendData(uint32_t ID, uint8_t data[]){
  //Uses can_due to send the data

//  CAN_FRAME outgoing;
  //uint32_t testIDvar = ID;
  //Serial.println(ID, HEX);
  outgoing.id = ID;
  outgoing.length = Max_len;
  for (int i = 0; i < 8; i++){
    outgoing.data.bytes[i] = data[i];
  }
  Can1.watchFor();
//  Can0.sendFrame(outgoing);
  //Serial.println("Sent");

}
*/

/**
* Converts a hex char to Byte
*/
uint8_t toByte(char data){
  uint8_t value = 0;
  if (data >= '0' && data <= '9'){
    return data - 48;
  }else if (data >= 'A' && data <= 'F'){
    return data - 55;
  }else{
    return 0;
  }
}

/**
* Used in the readCAN method
*/
String const_char(uint32_t data){
    String msg = "";
    for (int i = 0; i < 2; i++){
        uint32_t mask = 0xF;
        uint32_t masked_data = data & mask<<(i*4);
        masked_data = masked_data>>(i*4);
        msg = String(String(masked_data, HEX) + msg);
    }
    return msg;
}

/**
* Method to handle messages coming through the serial
*/
void serialEvent(){
    //Serial.println("serial event method");
    String msg = Serial.readString();
    msg.trim();
    String prefix = msg.substring(0,3);
    if (prefix == "SET"){
      //number are off for substring
      String idString = msg.substring(6,9); // would have the same length in the string
      idString.trim();
      String dataString;
      int id;
      /*
      if(idString == "DAC"){
        if(msg.substring(6,10) == "DAC0"){
          //Serial.println("DAC0");
          id = DAC0;
        }
        else if(msg.substring(6,10) == "DAC1"){
          //Serial.println("DAC1");
          id = DAC1;
        }
        dataString = msg.substring(11);
      }
      else{
      */
        id = idString.toInt();
        dataString = msg.substring(10);
      //}
      dataString.trim();
      // get the data of the send message SET 000 0
      int data = dataString.toInt();
      if(msg.substring(4,5) == "A"){
        //Serial.println("analog");
        setDataAnalog(id, data);
      }
      else if(msg.substring(4,5) == "D"){
        //Serial.println("digital");
        setDataDigital(id, data);
      }
      // parse id and set pin using arduino functions
        /*int dataLength = msg.length()/9;
        // how many messages there are
        String msgData[dataLength]; // was string
        for (int k = 0; k < dataLength; k++){
            msgData[k] = msg.substring(k*9,(k+1)*9);
            //contains all of the send messages in an array
        }
        //Serial.println(msgData[0]);
        Serial.println("Finished getting messages");
        for (int j = 0; j < dataLength; j++){
            String idString = msgData[j].substring(4,7); // would have the same length in the string
            char buffer1[idString.length()];
            idString.toCharArray(buffer1, idString.length());
            int id = atoi(buffer1); // should change to an int
            // dont need to change anything else becuase it will just sent and check them
            // uint32_t id = (16*16 * toByte(idString.charAt(0)) + 16 * toByte(idString.charAt(1)) + toByte(idString.charAt(2)));
            String dataString = msgData[j].substring(8); // get the data of the send message SET 000 0
            char buffer2[dataString.length()];
            dataString.toCharArray(buffer2, dataString.length());
            int data = atoi(buffer2);
            // data[i/2] = (16 * toByte(stringByte.charAt(0)) + toByte(stringByte.charAt(1))); // Adds each byte to the array.
    
            setData(id, data); // send that id and the data
            // have an option to send analog data
        }
        */
    }

    if (prefix == "CHK"){
      // numbers are off for substring
      String idString = msg.substring(6,9); // would have the same length in the string
      int id = idString.toInt();
      String dataString = msg.substring(10); // get the data of the send message SET 000 0
      int data = dataString.toInt();
      if(msg.substring(4,5) == "A"){
        Serial.println(checkDataAnalog(id, data));
      }
      else if(msg.substring(4,5) == "D"){
        checkDataDigital(id, data);
      }
      //Serial.println(msg.substring(4,7));
      //Serial.println(msg.substring(8));
      // parse id and set pin using arduino functions
        /*int dataLength = msg.length()/9;
        // how many messages there are
        String msgData[dataLength]; // was string
        for (int k = 0; k < dataLength; k++){
            msgData[k] = msg.substring(k*9,(k+1)*9);
            //contains all of the send messages in an array
        }
        //Serial.println(msgData[0]);
        Serial.println("Finished getting messages");
        for (int j = 0; j < dataLength; j++){
            String idString = msgData[j].substring(4,7); // would have the same length in the string
            char buffer1[idString.length()];
            idString.toCharArray(buffer1, idString.length());
            int id = atoi(buffer1); // should change to an int
            // dont need to change anything else becuase it will just sent and check them
            // uint32_t id = (16*16 * toByte(idString.charAt(0)) + 16 * toByte(idString.charAt(1)) + toByte(idString.charAt(2)));
            String dataString = msgData[j].substring(8); // get the data of the send message SET 000 0
            char buffer2[dataString.length()];
            dataString.toCharArray(buffer2, dataString.length());
            int data = atoi(buffer2);
            // data[i/2] = (16 * toByte(stringByte.charAt(0)) + toByte(stringByte.charAt(1))); // Adds each byte to the array.
    
            setData(id, data); // send that id and the data
            // have an option to send analog data
        }
        */
    }
 /*
    if (prefix == "SND"){
        //sometimes the arduino cant read them fast enough, need to slow them down
        // will build up a buffer of multiple send messages and then check it

        //Serial.println("Getting data");
        int dataLength = msg.length()/24;
        //Serial.println(String(dataLength));
        String msgData[dataLength];
        for (int k = 0; k < dataLength; k++){
            msgData[k] = msg.substring(k*24,(k+1)*24);
            //Serial.println(msgData[k]);
        }
        //Serial.println("Finished getting messages");
        for (int j = 0; j < dataLength; j++){
            String idString = msgData[j].substring(4,7);
            //TODO: Write an actual good String to hex converter
            uint32_t id = (16*16 * toByte(idString.charAt(0)) + 16 * toByte(idString.charAt(1)) + toByte(idString.charAt(2)));
            String dataString = msgData[j].substring(8);      
            uint8_t data[8];
            for (int i = 0; i < 16; i+=2){
                //This loop goes through the string and gets all the hex data      
                String stringByte = dataString.substring(i,i+2);
                //Again, write an actual good string to hex converter
                 data[i/2] = (16 * toByte(stringByte.charAt(0)) + toByte(stringByte.charAt(1)));//Adds the each byte to the array.
            }
            sendData(id, data);
        }
    }
    */
    else if (prefix == "LOG"){
        state = Log;
        logData();
    }
    else if (prefix == "IDL"){
        state = Idle;
    }
}
