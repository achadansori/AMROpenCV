// Motor A
int enA = 38;
int inA1 = 22;
int inA2 = 24;
// Motor B
int enB = 40;
int inB1 = 26;
int inB2 = 28;
// Motor C
int enC = 42;
int inC1 = 30;
int inC2 = 32;
// Motor D
int enD = 44;
int inD1 = 34;
int inD2 = 36;
void setup() {
	// Set all the motor control pins to outputs
	pinMode(enA, OUTPUT);
	pinMode(enB, OUTPUT);
  pinMode(enC, OUTPUT);
	pinMode(enD, OUTPUT);
	pinMode(inA1, OUTPUT);
	pinMode(inA2, OUTPUT);
	pinMode(inB1, OUTPUT);
	pinMode(inB2, OUTPUT);
  pinMode(inC1, OUTPUT);
	pinMode(inC2, OUTPUT);
	pinMode(inD1, OUTPUT);
	pinMode(inD2, OUTPUT);
	
	// Turn off motors - Initial state
	digitalWrite(inA1, LOW);
	digitalWrite(inA2, LOW);
	digitalWrite(inB1, LOW);
	digitalWrite(inB2, LOW);
  digitalWrite(inC1, LOW);
	digitalWrite(inC2, LOW);
	digitalWrite(inD1, LOW);
	digitalWrite(inD2, LOW);
}

void forward () {
	digitalWrite(inA1, HIGH);
	digitalWrite(inA2, LOW);
	digitalWrite(inB1, HIGH);
	digitalWrite(inB2, LOW);
  digitalWrite(inC1, HIGH);
	digitalWrite(inC2, LOW);
	digitalWrite(inD1, HIGH);
	digitalWrite(inD2, LOW);
  analogWrite(enA, 150);
  analogWrite(enB, 150);
  analogWrite(enC, 150);
  analogWrite(enD, 150);
}
void stop () {
	digitalWrite(inA1, LOW);
	digitalWrite(inA2, LOW);
	digitalWrite(inB1, LOW);
	digitalWrite(inB2, LOW);
  digitalWrite(inC1, LOW);
	digitalWrite(inC2, LOW);
	digitalWrite(inD1, LOW);
	digitalWrite(inD2, LOW);
  analogWrite(enA, 150);
  analogWrite(enB, 150);
  analogWrite(enC, 150);
  analogWrite(enD, 150);
}

void loop() {
  stop();
  delay(1000);
}

