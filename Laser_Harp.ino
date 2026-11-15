// Laser harp firmware (Arduino Nano).
//
// Six laser beams each shine on a photoresistor (LDR). Each LDR sits in a
// voltage divider on one analog pin: LDR from +5V to the pin, 240 ohm from the
// pin to GND. A lit LDR pulls the pin up; a hand in the beam lets it fall.
//
// The board answers one question, "which beam is blocked?", and sends the
// answer to the laptop as a line of text ("A0" to "A5"). Laser_Harp.py turns
// that line into a note.

const int NUM_BEAMS = 6;
const int BEAM_PINS[NUM_BEAMS] = {A0, A1, A2, A3, A4, A5};
const char *const BEAM_NAMES[NUM_BEAMS] = {"A0", "A1", "A2", "A3", "A4", "A5"};

// analogRead() returns 0-1023. At or below this, the beam counts as blocked
// (190 is about 0.93 V on a 5 V reference).
const int BLOCKED_AT_OR_BELOW = 190;

// After a note is sent, wait this long before reading again.
const unsigned long HOLD_OFF_MS = 500;

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Beams are checked in order; the first blocked one is the note.
  for (int i = 0; i < NUM_BEAMS; i++) {
    if (analogRead(BEAM_PINS[i]) <= BLOCKED_AT_OR_BELOW) {
      Serial.println(BEAM_NAMES[i]);
      delay(HOLD_OFF_MS);
      return;
    }
  }
}
