# Laser Harp

A harp with laser beams for strings. Six lasers each shine on a light sensor. Put a hand in a beam and the harp plays that beam's note.

It's built in two halves. An Arduino Nano watches the beams and reports which one is blocked. A Python script on the laptop turns each report into a sound.

Write-up: [ashiswadhwani.in/blog/laser-harp](https://ashiswadhwani.in/blog/laser-harp)

## How it works

```
6 lasers ──light──> 6 photoresistors ──volts──> Arduino Nano ──USB serial──> Laser_Harp.py ──> speakers
                    (dividers on A0–A5)         "which beam is dark?"   "A0\n"   note map, NumPy synth,
                                                                                 simpleaudio
```

1. **Sensing.** Each beam lands on a photoresistor (LDR). The LDR and a 240 Ω resistor form a voltage divider on one analog pin. A lit LDR has a low resistance, so the pin sits near 5 V. A hand in the beam raises the LDR's resistance and the pin voltage drops.
2. **Deciding.** `Laser_Harp.ino` reads A0 to A5 in order. The first pin at or below **190** (out of 1023, about 0.93 V) is the blocked beam. The board prints its name (`A0` … `A5`) over serial and then waits **500 ms** before reading again.
3. **Playing.** `Laser_Harp.py` reads those lines, picks the note, and plays a one-second sine wave with an exponential fade (time constant 0.3 s), which gives it a plucked sound. Each note plays on its own thread, so notes can overlap and ring out.

| Beam | Pin | Note | Frequency |
|---|---|---|---|
| 1 | A0 | C4 | 261.63 Hz |
| 2 | A1 | D4 | 293.66 Hz |
| 3 | A2 | E4 | 329.63 Hz |
| 4 | A3 | F4 | 349.23 Hz |
| 5 | A4 | G4 | 392.00 Hz |
| 6 | A5 | A4 | 440.00 Hz |

### Behaviour to know about

- **One note at a time.** If two beams are blocked at once, the lower pin wins.
- **Holding a beam repeats the note** every half second, because of the 500 ms wait.
- **The threshold is fixed.** 190 suits the room it was tuned in. Under much brighter light, a blocked LDR may not read low enough; change `BLOCKED_AT_OR_BELOW` if so.

## Circuit

![Laser harp schematic](docs/schematic.svg)

Per channel (×6):

- LDR from **+5V** to the analog pin (A0 to A5).
- 240 Ω resistor from the same pin to **GND**.
- A laser module on **+5V** and **GND**, aimed at that LDR. The lasers are always on.

## Parts

- Arduino Nano and a USB cable
- 6 laser modules (5 V)
- 6 photoresistors (LDRs)
- 6 × 240 Ω resistors
- A laptop with speakers, running Python 3

## Running it

1. Upload `Laser_Harp.ino` to the Nano with the Arduino IDE.
2. Install the Python dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Find the Nano's serial port (Arduino IDE → Tools → Port) and start the player:
   ```
   python Laser_Harp.py COM3            # Windows
   python Laser_Harp.py /dev/ttyUSB0    # Linux
   ```
4. Break a beam.

Close the Arduino IDE's Serial Monitor first. Only one program can hold the port.

## Files

| File | What it is |
|---|---|
| `Laser_Harp.ino` | Arduino firmware: reads the six sensors, reports the blocked beam. |
| `Laser_Harp.py` | Laptop side: serial reader, note map, synth and playback. |
| `docs/schematic.svg` | The circuit, all six channels. |
| `requirements.txt` | Python dependencies. |
