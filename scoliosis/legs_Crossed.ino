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
  // map 함수로 0~1024까지의 값을 0~4095 값으로 단계를 나눠 매핑

  int result1 = abs(mfsr_r18a - mfsr_r18b);  //result1 = 양쪽 대퇴 이두쪽에 설치된 압력센서값의 차 / request_mode.py 에서의 val1 값
  int result2 = mfsr_r18e + mfsr_r18f;   // result2 = 기립근 쪽에 설치된 두 압력센서값의 합 / request_mode.py 에서의 val2 값

  Serial.println(result1);
  Serial.println(result2);
  

  delay(500);
}
