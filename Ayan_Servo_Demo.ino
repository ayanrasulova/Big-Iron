#include <Servo.h>

Servo wrist;
Servo thumb;
Servo pointer;
Servo middle;
Servo ring;
Servo pinky;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  wrist.attach(5);
  thumb.attach(6);
  pointer.attach(9);
  middle.attach(10);
  ring.attach(11);
  pinky.attach(3);


}

byte check_checksum(byte* buf) {
    byte check = buf[0];
    for (int i = 1; i < 6; ++i) {
        check ^= buf[i];
    }

    if (check == buf[6]) {
        return 1;
    }
    return 0;
}

void loop() {
  byte val = 0;
  byte checked = 0;
  byte vals[7]; 

  while (Serial.available() > 0) {
    val = Serial.read();
    if (val == 190) {  // start byte
        Serial.readBytes(vals, 7);

        checked = check_checksum(vals);
        if (checked) {
            Serial.println("Valid packet:");

            wrist.write(vals[0]);
            thumb.write(vals[1]);
            pointer.write(vals[2]);
            middle.write(vals[3]);
            ring.write(vals[4]);
            pinky.write(vals[5]);

            for (int i = 0; i < 6; ++i) {
                Serial.println(vals[i]);
            }

        } else {
            Serial.println("Checksum failed!!! Data collected:");
            for (int i = 0; i < 7; ++i) {
                Serial.println(vals[i]);
            }
        }
    } 
    else {
        Serial.print("Start byte not found! Instead found: ");
        Serial.println(val);
    }
  }
}