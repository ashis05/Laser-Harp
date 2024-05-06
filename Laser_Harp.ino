const int photoresistorPin0 = A0;
const int photoresistorPin1 = A1;
const int photoresistorPin2 = A2;
const int photoresistorPin3 = A3;
const int photoresistorPin4 = A4;
const int photoresistorPin5 = A5;
//String incomingByte;

void setup() {
  // Start serial communication
  Serial.begin(9600);
}

void loop() {
  // Read the value from the photoresistor
  int photoresistorValue0 = analogRead(photoresistorPin0);
  int photoresistorValue1 = analogRead(photoresistorPin1);
  int photoresistorValue2 = analogRead(photoresistorPin2);
  int photoresistorValue3 = analogRead(photoresistorPin3);
  int photoresistorValue4 = analogRead(photoresistorPin4);
  int photoresistorValue5 = analogRead(photoresistorPin5);
  
 /* Serial.println(photoresistorValue0);
  Serial.println(photoresistorValue1);
  Serial.println(photoresistorValue2);
  Serial.println(photoresistorValue3);
  Serial.println(photoresistorValue4);
  delay(19000);*/
  if (photoresistorValue0 <=190)
  {Serial.println("A0");
  delay(500);}
  else if (photoresistorValue1 <=190)
  {Serial.println("A1");
  delay(500);}
  else if (photoresistorValue2 <=190)
  {Serial.println("A2");
  delay(500);}
  else if (photoresistorValue3 <=190)
  {Serial.println("A3");
  delay(500);}
  else if (photoresistorValue4 <=190)
  {Serial.println("A4");
  delay(500);}
  else if (photoresistorValue5 <=190)
  {Serial.println("A5");
  delay(500);}
}
