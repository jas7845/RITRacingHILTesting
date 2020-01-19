#include <stdio.h>
#include <due_can.h>
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
  printf("in loop main");
  Can0.begin(CAN_BPS_500K);
  Can1.begin(CAN_BPS_500K);
  Serial.println("setup");
  serialEvent();
  Serial.begin(115200);
  Serial.setTimeout(2);
}

/**
* Logs the data by calling the readCAN method
*/
void logData(){
//keep the same
  //Continuously read data
    readCAN();
    //delay(1);
}

/**
* Does something
*/
void readCAN(){
  Can0.watchFor();
  String msg = "";
  CAN_FRAME incoming;
  if(Can0.available()>0){
    Can0.read(incoming);
    //Serial.print(const_char(incoming.id));
    //Serial.print(String(incoming.id));
    //Serial.print(" ");
    for (int i = 0; i < 8; i++){
        //Serial.print(const_char(incoming.data.bytes[i]));
        //Serial.print(String(incoming.data.bytes[i]));
    }
    //Serial.print("\n");
  }
}

/**
* need to change the CAN, not sure what to
* Arduino Method in the Arduino IDE
*/
void loop() {
  // put your main code here, to run repeatedly:
  //printf("in loop main");
  switch(state){
    case Log: logData();
    case Idle:;//Do nothing if Idling
  }
}

/**
* Method to handle messages coming through the serial
*/
void serialEvent(){
    Serial.println("serial event method");
    String msg = Serial.readString();
    String prefix = msg.substring(0,4);
    Serial.println(msg);
    if (prefix ==  "SET"){
    // parse id and set pin using arduino functions
        int dataLength = msg.length()/9;
        // how many messages there are
        Serial.println(String(dataLength));
        String msgData[dataLength]; // was string
        for (int k = 0; k < dataLength; k++){
            msgData[k] = msg.substring(k*9,(k+1)*9);
            //contains all of the send messages in an array
            Serial.println(msgData[k]);
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
    }
    else if (prefix ==  "CHK"){
    // parse id and set pin using arduino functions
        int dataLength = msg.length()/9;
        // how many messages there are
        //Serial.println(String(dataLength));
        String msgData[dataLength];
        for (int k = 0; k < dataLength; k++){
            msgData[k] = msg.substring(k*9,(k+1)*9);
            //contains all of the send messages in an array
            //Serial.println(msgData[k]);
        }
        //Serial.println("Finished getting messages");
        for (int j = 0; j < dataLength; j++){
            String idString = msgData[j].substring(4,7); // would have the same length in the string
            int ln = idString.length();
            char buffer1[ln];
            idString.toCharArray(buffer1, idString.length());
            int id = atoi(buffer1); // should change to an int
            // dont need to change anything else becuase it will just sent and check them
            // uint32_t id = (16*16 * toByte(idString.charAt(0)) + 16 * toByte(idString.charAt(1)) + toByte(idString.charAt(2)));
            String dataString = msgData[j].substring(8); // get the data of the send message SET 000 0
            char buffer2[dataString.length()]; //= char[dataString.length];
            dataString.toCharArray(buffer2, dataString.length());
            int data = atoi(buffer2);
            // data[i/2] = (16 * toByte(stringByte.charAt(0)) + toByte(stringByte.charAt(1))); // Adds each byte to the array.

            checkData(id, data); // send that id and the data
            // have an option to send analog data
        }
    }
    else if (prefix == "SND"){
    // this is what he has for send
        //Serial.println("Getting data");
        int dataLength = msg.length()/24;
        // how many messages there are
        // what is the message supposed to be and why divide it by 24?
        // 3 + 1 + 3 + 1 + 16 = 24 (he requires the pin to be three dig)
        //Serial.println(String(dataLength));
        String msgData[dataLength];
        for (int k = 0; k < dataLength; k++){
            msgData[k] = msg.substring(k*24,(k+1)*24);
            //contains all of the send messages in an array

            //Serial.println(msgData[k]);
        }
        //Serial.println("Finished getting messages");
        for (int j = 0; j < dataLength; j++){
            String idString = msgData[j].substring(4,7);
            //TODO: Write an actual good String to hex converter
            uint32_t id = (16*16 * toByte(idString.charAt(0)) + 16 * toByte(idString.charAt(1)) + toByte(idString.charAt(2)));
            String dataString = msgData[j].substring(8); // get the data of the send message
            uint8_t data[8];
            for (int i = 0; i < 16; i+=2){ // conver into integer value
                //This loop goes through the string and gets all the hex data
                String stringByte = dataString.substring(i,i+2);
                //Again, write an actual good string to hex converter
                data[i/2] = (16 * toByte(stringByte.charAt(0)) + toByte(stringByte.charAt(1)));//Adds the each byte to the array.
            }
            sendData(id, data); // send that id and the data
            // have an option to send analog data
        }
    }
    else if (prefix == "LOG"){
        state = Log;
        logData();
    }
    else if (prefix == "IDL"){
        state = Idle;
    }
}
/**
* Sets a pin either high or low based on the data
*/
void setData(int id, int data){
    pinMode(id, INPUT);
    printf("in setDATA main");
    if(data == 1){
        Serial.println("HIGH");
        digitalWrite(id, HIGH);
        //printf("set high");
    }
    else{
        Serial.println("LOW");
        digitalWrite(id, LOW);
        //printf("set low");
    }
    // what is the purpose of the delay
    //delay(1000);
}

/**
* Sets a pin either high or low based on the data
*/
int checkData(int id, int data){
    int pinData = digitalRead(id);
    if(pinData == 1){
        printf("check high");
        return 1;
    }
    else{
        printf("check low");
        return 0;
    }
}

// keep the same
/**
* Sends data to a pin
*/
void sendData(uint32_t ID, uint8_t data[]){
  //Uses can_due to send the data

  CAN_FRAME outgoing;
  //uint32_t testIDvar = ID;
  //Serial.println(ID, HEX);
  outgoing.id = ID;
  outgoing.length = Max_len;
  for (int i = 0; i < 8; i++){
    outgoing.data.bytes[i] = data[i];
  }
  Can1.watchFor();
  Can0.sendFrame(outgoing);
  //Serial.println("Sent");

}


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
