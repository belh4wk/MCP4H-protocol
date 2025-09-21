// MCP4H-L1 Arduino WindSim Example
// Minimal line-protocol parser for SimHub → MCP4H → Arduino
// Fan PWM on D9, LED on D6

const int FAN_PIN = 9;
const int LED_PIN = 6;

float speed_mps = 0.0f;
int gear = 0;

void setup() {
  pinMode(FAN_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);
}

void applyOutputs() {
  // Map 0..100 m/s to 0..255 PWM (tune to your rig)
  float clamped = speed_mps;
  if (clamped < 0) clamped = 0;
  if (clamped > 100) clamped = 100;
  int pwm = (int)(clamped * 2.55); // simple linear map
  analogWrite(FAN_PIN, pwm);

  // Simple gear -> LED brightness (0 = off)
  if (gear <= 0) {
    analogWrite(LED_PIN, 0);
  } else {
    int led = map(gear, 1, 8, 32, 255); // gears 1..8
    analogWrite(LED_PIN, led);
  }
}

void loop() {
  static char line[160];
  static uint8_t idx = 0;

  while (Serial.available()) {
    char c = (char)Serial.read();
    if (c == '\n' || idx >= sizeof(line)-1) {
      line[idx] = '\0';

      // Expect tokens: MCP4H v=1 ts=... spd_mps=.. gear=..
      char *tok = strtok(line, " ");
      while (tok) {
        if (strncmp(tok, "spd_mps=", 8) == 0) {
          speed_mps = atof(tok + 8);
        } else if (strncmp(tok, "gear=", 5) == 0) {
          gear = atoi(tok + 5);
        }
        tok = strtok(NULL, " ");
      }
      applyOutputs();
      idx = 0;
    } else {
      line[idx++] = c;
    }
  }
}
