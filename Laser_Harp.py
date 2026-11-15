"""Laser harp: the laptop half.

Reads beam events from the Arduino over USB serial (one line per event, "A0"
to "A5") and plays a note for each one.

    python Laser_Harp.py            # uses COM3
    python Laser_Harp.py /dev/ttyUSB0
"""

import argparse
import threading

import numpy as np
import serial
import simpleaudio as sa

SAMPLE_RATE = 44100  # Hz
NOTE_SECONDS = 1.0  # length of each note
DECAY_SECONDS = 0.3  # time constant of the exponential fade

# Beam -> (note, frequency in Hz). Six white keys up from middle C.
NOTES = {
    "A0": ("C", 261.63),
    "A1": ("D", 293.66),
    "A2": ("E", 329.63),
    "A3": ("F", 349.23),
    "A4": ("G", 392.00),
    "A5": ("A", 440.00),
}


def note_wave(frequency, duration=NOTE_SECONDS, decay=DECAY_SECONDS):
    """A sine at `frequency` that starts at half volume and fades exponentially."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    envelope = np.exp(-t / decay)
    return 0.5 * envelope * np.sin(2 * np.pi * frequency * t)


def play(samples):
    """Play 16-bit mono samples and block until they finish."""
    sa.play_buffer(samples, 1, 2, SAMPLE_RATE).wait_done()


def main():
    parser = argparse.ArgumentParser(description="Laser harp sound player")
    parser.add_argument("port", nargs="?", default="COM3", help="serial port of the Arduino")
    parser.add_argument("--baud", type=int, default=9600)
    args = parser.parse_args()

    # Each note is synthesised once, up front, as 16-bit PCM.
    sounds = {
        beam: (note_wave(freq) * 32767).astype(np.int16) for beam, (_, freq) in NOTES.items()
    }

    ser = serial.Serial(args.port, args.baud)
    print(f"Listening on {args.port} at {args.baud} baud. Ctrl+C to stop.")
    try:
        while True:
            line = ser.readline().decode("utf-8", errors="ignore").strip()
            if line in sounds:
                print(f"{line} -> {NOTES[line][0]}")
                # One thread per note, so notes overlap and ring out.
                threading.Thread(target=play, args=(sounds[line],), daemon=True).start()
            else:
                print("off")
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()
        print("Serial connection closed.")


if __name__ == "__main__":
    main()
