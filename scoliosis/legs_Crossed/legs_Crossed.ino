int SensorPin = A0; // analog pin 0
int SensorPin2 = A1;
int SensorPin3 = A2;
int SensorPin4 = A3;
int SensorPin5 = A4;
int SensorPin6 = A5;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int SensorReading = analogRead(SensorPin);
  int SensorReading2 = analogRead(SensorPin2);
  int SensorReading3 = analogRead(SensorPin3);
  int SensorReading4 = analogRead(SensorPin4);
  int SensorReading5 = analogRead(SensorPin5);
  int SensorReading6 = analogRead(SensorPin6);

  int mfsr_r18a = map(SensorReading, 0, 1024, 0, 4095);
  int mfsr_r18b = map(SensorReading2, 0, 1024, 0, 4095);
  int mfsr_r18c = map(SensorReading3, 0, 1024, 0, 4095);
  int mfsr_r18d = map(SensorReading4, 0, 1024, 0, 4095);
  int mfsr_r18e = map(SensorReading5, 0, 1024, 0, 4095);
  int mfsr_r18f = map(SensorReading6, 0, 1024, 0, 4095);

// Serial.print("1st sensor(대퇴이두 (왼쪽)):");
// Serial.println(mfsr_r18a);
//  Serial.print("2nd sensor(대퇴이두 (오른쪽)):");
//  Serial.println(mfsr_r18b);
//  Serial.print("3rd (둔근(왼쪽)):");
//  Serial.println(mfsr_r18c);
//  Serial.print("4th sensor(둔근(오른쪽)):");
//  Serial.println(mfsr_r18d);
//  Serial.print("5th sensor(기립근(왼쪽)):");
//  Serial.println(mfsr_r18e);
//  Serial.print("6th sensor(기립근(오른쪽)):");
//  Serial.println(mfsr_r18f);

  int result1 = abs(mfsr_r18a - mfsr_r18b);  //result1 150이상 되면 메시지 전송
  int result2 = mfsr_r18e + mfsr_r18f;   // result2 값이 1000이상 되면 메시지 전송


  Serial.println(result1);
  Serial.println(result2);
  

  // 둔근에 압력이 감지 될 때 대퇴이두 센서 출력값이 150 이상이면 다리 꼬지 마세요 출력 
  //if ((abs(SensorReading - SensorReading2) >= 150) && (SensorReading3 != 0) && (SensorReading4 != 0)) {
   // Serial.println("다리 꼬지 마세요!");
  //}

  // 기립근에 일정 수준 이상의 압력 감지시 허리 피세요! 출력
  //if ((SensorReading5 >= 40) && (SensorReading6 >= 40)) {
    //Serial.println("허리 피세요!");
  //}

  delay(1000);
}
