# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 19:06:53 2020

@author: Rui
"""

import mido
import numpy as np

def noteexport(net_num,net_note_data,net_note_matrix,coll_matrix,chan_num,max_cir,ticks_per_beat,sample_t):
    out_matrix = net_note_matrix
    out_midi = mido.MidiFile()
    out_midi.ticks_per_beat = ticks_per_beat
    track = mido.MidiTrack()
    out_midi.tracks.append(track)
    #outport = mido.open_output('Microsoft GS Wavetable Synth')
    #track.append(mido.Message('program_change', program=0, time=0))
    
    out_txt = []
    event_time = 0
    event_tic = 0
    tic = np.zeros(net_num) # store note states
    for i in range(max_cir):
        for j in range(len(chan_num)):
            channelA = int(chan_num[j])
            pg_matrix = coll_matrix[0][j]
            ctl_matrix = coll_matrix[1][j]
            pch_matrix = coll_matrix[2][j]
            aft_matrix = coll_matrix[3][j]            
            if pg_matrix[i]!=-1:
                programA = int(pg_matrix[i])
                out_txt.append('program_change channel='+str(channelA)+' program='+str(programA)+' time='+str(event_time))
                track.append(mido.Message('program_change', channel=channelA, program=programA, time=event_tic))
                event_time = 0
                event_tic = 0    
            if ctl_matrix[0][i]!=-1:
                controlA = int(ctl_matrix[0][i])
                valueA = int(ctl_matrix[1][i])
                out_txt.append('control_change channel='+str(channelA)+' control='+str(controlA)+' value='+str(valueA)+' time='+str(event_time))
                track.append(mido.Message('control_change', channel=channelA, control=controlA, value=valueA, time=event_tic))
                event_time = 0
                event_tic = 0
            if pch_matrix[i]!=-1:
                pitchA = int(pch_matrix[i])
                out_txt.append('pitchwheel channel='+str(channelA)+' pitch='+str(pitchA)+' time='+str(event_time))
                track.append(mido.Message('pitchwheel', channel=channelA, pitch=pitchA, time=event_tic))
                event_time = 0
                event_tic = 0   
            if aft_matrix[i]!=-1:
                valueA = int(aft_matrix[i])
                out_txt.append('aftertouch channel='+str(channelA)+' value='+str(valueA)+' time='+str(event_time))
                track.append(mido.Message('aftertouch', channel=channelA, value=valueA, time=event_tic))
                event_time = 0
                event_tic = 0
            
        for j in range(net_num):
            channelA = net_note_data[j][0]
            noteA = net_note_data[j][1]
            velocityA = out_matrix[j,i]
            if velocityA!=tic[j]:
                if tic[j]>0:  # currently note on
                    out_txt.append('note_off channel='+str(channelA)+' note='+str(noteA)+' velocity=0 time='+str(event_time))
                    track.append(mido.Message('note_off', channel=channelA, note=noteA, velocity=0, time=event_tic))
                    #print(str(event_tic))
                    tic[j] = velocityA
                    event_time = 0
                    event_tic = 0
                    if velocityA>0:
                        out_txt.append('note_on channel='+str(channelA)+' note='+str(noteA)+' velocity='+str(int(velocityA))+' time=0')
                        track.append(mido.Message('note_on', channel=channelA, note=noteA, velocity=int(velocityA), time=0))
                    continue
                if tic[j]==0: # currently note off
                    out_txt.append('note_on channel='+str(channelA)+' note='+str(noteA)+' velocity='+str(int(velocityA))+' time='+str(event_time))
                    track.append(mido.Message('note_on', channel=channelA, note=noteA, velocity=int(velocityA), time=event_tic))
                    #print(str(event_tic))
                    tic[j] = velocityA
                    event_time = 0
                    event_tic = 0
        event_time = event_time+sample_t
        event_tic = event_tic+1        
    
    return out_txt,out_midi