import serial
import time
import numpy as np
import simpleaudio as sa
import threading

# Define the notes and their frequencies
note_frequencies = {
    "C": 261.63,
    "D": 293.66,
    "E": 329.63,
    "F": 349.23,
    "G": 392.00,
    "A": 440.00,
}

# Function to generate a waveform for a given note with an envelope
def generate_note_wave(frequency, duration, attack_time=0.05, decay_time=0.3, sampling_rate=44100):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    
    # Create an envelope with an exponential decay
    envelope = np.exp(-t / decay_time)
    
    # Generate the waveform with the envelope
    wave = 0.5 * envelope * np.sin(2 * np.pi * frequency * t)
    return wave

# Function to play a note in a separate thread
def play_note_thread(note, duration=1.0):
    threading.Thread(target=play_note, args=(note, duration)).start()

# Function to play a note
def play_note(note, duration=1.0):
    frequency = note_frequencies.get(note, 0)
    if frequency == 0:
        print(f"Invalid note: {note}")
        return
    
    wave = generate_note_wave(frequency, duration)
    audio_data = (wave * 32767).astype(np.int16)
    sa.play_buffer(audio_data, 1, 2, 44100).wait_done()

# Replace 'COM3' with the appropriate serial port your Arduino is connected to
serial_port = 'COM3'
baud_rate = 9600

# Open the serial connection
ser = serial.Serial(serial_port, baud_rate)
music=[]

try:
    while True:
        # Read a line from the serial port
        i = ser.readline().decode('utf-8').strip()

        a0 = "C"
        a1 = "D"
        a2 = "E"
        a3 = "F"
        a4 = "G"
        a5 = "A"
        b = "off"

        # Check the received input and send the corresponding command to Arduino
        if i == "A0":
            music.append(a0)
            print("a0")
        elif i == "A1":
            music.append(a1)
            print("a1")
        elif i == "A2":
            music.append(a2)
            print("a2")
        elif i == "A3":
            music.append(a3)
            print("a3")
        elif i == "A4":
            music.append(a4)
            print("a4")
        elif i == "A5":
            music.append(a5)
            print("a5")
        else:
            print(b)

        for note in music:
            play_note_thread(note) # Optional delay between notes to avoid overlapping

        music.clear()
            
except KeyboardInterrupt:
    # Close the serial connection when the program is interrupted
    ser.close()
    print("Serial connection closed.")
