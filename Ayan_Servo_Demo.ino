#include <Servo.h>

Servo myservo;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  myservo.attach(5);

}

char check_checksum (char* buf){
    char check = buf[0];
    for (int i = 1; i < 6; ++i){
        check ^= buf[i];
    }

    if (check == buf[6]){
        return 1;
    }
}

void loop() {
  // put your main code here, to run repeatedly:
  char val = 0;
  char checked = 0;
  char* vals;

  while (Serial.available() != 0){
    val = Serial.read();
    if (val == 190){ // start byte found
        Serial.readBytes(vals, 7); 
        checked = check_checksum(vals);
        if (checked){
            for (int i = 0; i<6; ++i){
                Serial.println(vals[i]);
                myservo.write(vals[0]);
            }
        }
        else {
          Serial.println("Checksum failed!!! Data collected: ");
           for (int i = 0; i<7; ++i){
                Serial.println(vals[i]);
            }
        }


    }
    else {
      Serial.print("Start byte not found! Insted found ");
      Serial.println(val);
    }

  }


}

