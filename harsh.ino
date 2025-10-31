// SIT210 Task 4.2C - Multiple Interrupts (Button + Ultrasonic Sensor)
// Harshpreet Singh Raju
// Arduino Nano 33 IoT

const int buttonPin = 2;   // Push button
const int trigPin = 3;     // Ultrasonic TRIG
const int echoPin = 4;     // Ultrasonic ECHO
const int led1 = 8;        // LED1 controlled by button
const int led2 = 9;        // LED2 controlled by sensor

volatile bool led1State = LOW;
volatile bool led2State = LOW;

volatile unsigned long startMicro = 0;
volatile unsigned long durationMicro = 0;
volatile bool newReading = false;

// ISR for button press
void buttonISR() {
  led1State = !led1State;
  digitalWrite(led1, led1State);
  Serial.println("Button interrupt: LED1 toggled");
}

// ISR for ultrasonic echo
void echoISR() {
  if (digitalRead(echoPin) == HIGH) {
    startMicro = micros();  // rising edge
  } else {
    durationMicro = micros() - startMicro;  // falling edge
    newReading = true;
  }
}

void setup() {
  Serial.begin(9600);

  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);

  digitalWrite(led1, LOW);
  digitalWrite(led2, LOW);

  // Attach interrupts
  attachInterrupt(digitalPinToInterrupt(buttonPin), buttonISR, FALLING);
  attachInterrupt(digitalPinToInterrupt(echoPin), echoISR, CHANGE);

  Serial.println("System Ready — Waiting for interrupts...");
}

void loop() {
  // Trigger ultrasonic sensor periodically
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  delay(100);

  if (newReading) {
    newReading = false;
    float distance = durationMicro * 0.034 / 2.0; // cm
    Serial.print("Distance: ");
    Serial.print(distance);
    Serial.println(" cm");

    if (distance > 0 && distance < 20) {
      led2State = !led2State;
      digitalWrite(led2, led2State);
      Serial.println("Ultrasonic interrupt: LED2 toggled");
    }
  }
}
