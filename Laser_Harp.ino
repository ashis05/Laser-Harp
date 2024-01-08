String incomingByte ;  

int LDR1 = A0;

void setup() {

  Serial.begin(9600);

  pinMode(LED_BUILTIN, OUTPUT);

  pinMode(LDR1, INPUT);

}
void loop() {

  if (Serial.available() > 0) {

    int SLDR1 = analogRead(LDR1);
      if (SLDR1 <= 400){//if the photoresistor detects less light it plays a note
      Serial.write("on");
      }
      else{//if the photoresistor detects  more light it stops the note
      Serial.write("off");
      }
      delay(1000);
    /*incomingByte = Serial.readStringUntil('\n');

    if (incomingByte == "on") {

      digitalWrite(LED_BUILTIN, HIGH);

      Serial.write("Led on");

      delay(1000);
    }

    else if (incomingByte == "off") {

      digitalWrite(LED_BUILTIN, LOW);

      Serial.write("Led off");

      delay(1000);
    }

    else{

     Serial.write("invald input");

     delay(1000);

    }*/

  }

}
