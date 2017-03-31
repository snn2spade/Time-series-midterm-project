import cv2
import numpy as np

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import write_midi_jinc as midi
from midiutil.MidiFile3 import MIDIFile
import image_process_option as opt
import copy

item_name = 'circle'
item_name2 = item_name
img = cv2.imread('/Users/snn2spade/Desktop/'+item_name+'_1.png')
img2 = cv2.imread('/Users/snn2spade/Desktop/'+item_name2+'_1.png')
gen_midi = False

# Canny edge detection
edge_1 = cv2.Canny(img,100,200)
edge_2 = cv2.Canny(img2,100,200)

# Image resizing
edge_1_h = edge_1.shape[0]
edge_1_w = edge_1.shape[1]
edge_1_ratio = 52/edge_1_h
edge_1_h = 52
edge_1_w = int(edge_1_w * edge_1_ratio)
edge_1 = cv2.resize(edge_1,(edge_1_w,edge_1_h), interpolation = cv2.INTER_AREA)
print("width-img1:"+str(edge_1_w))


edge_2_h = edge_2.shape[0]
edge_2_w = edge_2.shape[1]
edge_2_ratio = 52/edge_2_h
edge_2_h = 52
edge_2_w = int(edge_2_w * edge_2_ratio)
edge_2 = cv2.resize(edge_2,(edge_2_w,edge_2_h),interpolation= cv2.INTER_AREA)
print("width-img2:"+str(edge_2_w))

# Convert to binary B&W
(thresh, edge_1_bw) = cv2.threshold(edge_1, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
(thresh, edge_2_bw) = cv2.threshold(edge_2, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

# Output
plt.subplot(121),plt.imshow(edge_1_bw,'gray')
plt.title(item_name+'_1'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edge_2_bw,'gray')
plt.title(item_name2+'_2'), plt.xticks([]), plt.yticks([])
# plt.imshow(edge_1_bw,'gray')

################ midi processing ################

track = 0
channel = 0
time = 0  # In beats
duration = 1  # In beats
tempo = 120 # In BPM
volume = 120  # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track
# automatically created)
MyMIDI.addTempo(track, time, tempo)
MyMIDI.addTrackName(track,time,item_name+" Track")

MyMIDI2 = MIDIFile(1)  # One track, defaults to format 1 (tempo track
# automatically created)
MyMIDI2.addTempo(track, time, tempo)
MyMIDI2.addTrackName(track,time,item_name2+ "Track")

MyMIDI3 = MIDIFile(1)  # One track, defaults to format 1 (tempo track
# automatically created)
MyMIDI3.addTempo(track, time, tempo)
MyMIDI3.addTrackName(track,time,item_name+" Track")

####### connect line between note test #######
def draw_line_in_note(array ,height ,width):
    edge_1_copy = copy.deepcopy(array)
    for y in range(height):
        for x in range(width):
            if edge_1_copy[y][x] > 0:
                count = 0
                x_index = x + 1
                while x_index < width and edge_1_copy[y][x_index] > 0:
                    count += 1
                    edge_1_copy[y][x_index] = 0
                    x_index += 1
                edge_1_copy[y][x] = 1 + count
    return edge_1_copy
edge_1_bw_connected = draw_line_in_note(edge_1_bw,edge_1_h,edge_1_w)
edge_2_bw_connected = draw_line_in_note(edge_2_bw,edge_2_h,edge_2_w)

for x in range(edge_1_w):
    for y in range(edge_1_h):
        if edge_1_bw_connected[y][x] > 0:
            MyMIDI.addNote(track, channel, midi.getPitch(52-y), time, edge_1_bw_connected[y][x], volume)
    time += 1

time = 0
for x in range(edge_2_w):
    for y in range(edge_2_h):
        if edge_2_bw_connected[y][x] > 0:
            MyMIDI2.addNote(track, channel, midi.getPitch(52-y), time, edge_2_bw_connected[y][x], volume)
    time += 1

time = 0
for x in range(edge_1_w):
    for y in range(edge_1_h):
        if edge_1_bw[y][x] > 0:
            MyMIDI3.addNote(track, channel, midi.getPitch(52-y), time, duration, volume)
    time += 1

if gen_midi:
    with open(item_name+"-1.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)
    with open(item_name2+"-2.mid", "wb") as output_file2:
        MyMIDI2.writeFile(output_file2)
    with open(item_name+"-1-non-connected.mid", "wb") as output_file3:
        MyMIDI3.writeFile(output_file3)

plt.show()
