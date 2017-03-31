#!/usr/bin/env python

from midiutil.MidiFile3 import MIDIFile


def getPitch(i):
    pitch = i + 21
    add = i % 7
    mul = int((i - 1) / 7)
    if add == 0:
        pitch += 0
    elif add <= 2:
        pitch += 1
    elif add == 3:
        pitch += 2
    elif add <= 5:
        pitch += 3
    elif add == 6:
        pitch += 4
    elif add == 7:
        pitch += 5
    return pitch + (mul * 5)


# MIDI note number
degrees = []
for i in range(0, 8):
    degrees.append([])
    for j in range(0, 52):
        degrees[i].append(1)

track = 0
channel = 0
time = 0  # In beats
duration = 1  # In beats
tempo = 60  # In BPM
volume = 120  # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track
# automatically created)
MyMIDI.addTempo(track, time, tempo)
# MyMIDI.addTrackName(track,time,"Sample Track")

for row in degrees:
    for i in range(len(row)):
        if row[i] == 1:
            MyMIDI.addNote(track, channel, getPitch(i), time, duration, volume)

    time = time + 1

with open("test.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)
