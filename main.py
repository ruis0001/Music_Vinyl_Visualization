# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 12:25:50 2020

@author: Rui
"""

# OTHER FUNCTIONS
import mido
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
from z_notelib import note_name,note_freq # read in note library
from z_noteplot import noteplot
from z_noteexport import noteexport
# ------------------------------------------------------------------ #
# SET AMPLIFIER
mido.set_backend('mido.backends.pygame')
#outport = mido.open_output('Microsoft GS Wavetable Synth')
# ------------------------------------------------------------------ #
# READ MIDI FILE
file_dir = 'source/'
#song_name = 'Queen_-_Another_One_Bites_the_Dust'
song_name = 'Queen_-_Bohemian_Rhapsody'
#song_name = 'Queen_-_i_want_to_break_free'
#song_name = 'Queen_-_Radio_Ga_Ga'
#song_name = 'Queen_-_Too_Much_Love_Will_Kill_You'
#song_name = 'Queen_-_We_Are_The_Champions'
#song_name = 'Queen_-_We_Are_The_Champions'
#song_name = u'刀剑如梦'
#song_name = u'千千阙歌'
#song_name = u'海阔天空'
#song_name = 'myheart'
#song_name = 'beethoven_ode_to_joy'
memFile = mido.MidiFile(file_dir+song_name+'.mid')
# ------------------------------------------------------------------ #
# IMPORT
rawtxt = []
for msg in memFile.play():
    print(msg)
    #outport.send(msg) # play MIDI
    rawtxt.append(str(msg))
print('Finish reading MIDI file...')
#outport.close() 
# ------------------------------------------------------------------ #
# OBTAIN FILE PROPERTIES
songlen = 0
tempo = mido.bpm2tempo(120)/1000000 # in sec
sample_t = tempo/memFile.ticks_per_beat # in sec
print('Sampling Rate = '+str(int(1/sample_t))+' sample/sec')
chan_num = []
total_note_data = []
for i in rawtxt:
    k = [m for m in range(len(i)) if i.startswith('=', m)]
    t = [m for m in range(len(i)) if i.startswith(' ', m)]
    time = float(i[k[-1]+1:len(i)])
    if time>0:
        songlen = songlen+time  
    if str(i)[0:4]=='note':
        note = int(i[k[1]+1:t[2]])    
        if note in note_name:
            if note not in total_note_data:
                total_note_data.append(note)
            channel = int(i[k[0]+1:t[1]])
            if channel not in chan_num:
                chan_num.append(channel) 
max_cir = int(1/sample_t*songlen)
total_note_data = list(sorted(total_note_data))
chan_num = sorted(chan_num)
# ------------------------------------------------------------------ #
# DATA EXTRACTION
notetxt = []
progtxt = []
ctrltxt = []
pitchtxt = []
aftchtxt = []
this_time_note = 0  # stored note text are in delta time
this_time_prog = 0
this_time_ctrl = 0   # stored control text are in delta time
this_time_pitch = 0
this_time_aftch = 0
for i in rawtxt:
    k = [m for m in range(len(i)) if i.startswith('=', m)]
    t = [m for m in range(len(i)) if i.startswith(' ', m)]
    time = float(i[k[-1]+1:len(i)])
    if time>0:
        this_time_ctrl = this_time_ctrl+time    
        this_time_note = this_time_note+time
        this_time_prog = this_time_prog+time
        this_time_pitch = this_time_pitch+time
        this_time_aftch = this_time_aftch+time
    if i[0:4]=="note":
        notetxt.append(i[0:k[-1]+1]+str(this_time_note))
        this_time_note = 0
    elif i[0:4]=='prog':
        progtxt.append(i[0:k[-1]+1]+str(this_time_prog))
        this_time_prog = 0
    elif i[0:4]=='cont':
        ctrltxt.append(i[0:k[-1]+1]+str(this_time_ctrl))
        this_time_ctrl = 0
    elif i[0:4]=='pitc':
        pitchtxt.append(i[0:k[-1]+1]+str(this_time_pitch))
        this_time_pitch = 0
    elif i[0:4]=='afte':
        aftchtxt.append(i[0:k[-1]+1]+str(this_time_aftch))
        this_time_aftch = 0

total_index = {}
total_note_matrix = []
total_sequal = []
total_sequal_abs = []
total_sequal2 = []
total_sequal_abs2 = []
lap_note_matrix = np.zeros((len(total_note_data),max_cir))
lap_sequal2 = np.full((len(total_note_data),6000),-1)
lap_sequal_abs2 = np.full((len(total_note_data),6000),-1)
net_num = 0
net_note_data = []
prog_matrix = np.zeros((len(chan_num),max_cir))
ctrl_matrix = np.zeros((len(chan_num),2,max_cir))
pitch_matrix = np.zeros((len(chan_num),max_cir))
aftch_matrix = np.zeros((len(chan_num),max_cir))

for chan_sel in chan_num:
    pgtxt = []
    this_time = 0    
    for i in progtxt:
        k = [m for m in range(len(i)) if i.startswith('=', m)]
        t = [m for m in range(len(i)) if i.startswith(' ', m)]
        channel = int(i[k[0]+1:t[1]])
        time = float(i[k[-1]+1:len(i)])
        if time>0:
            this_time = this_time+time
        if channel==chan_sel:
            pgtxt.append(i[0:k[-1]+1]+str(this_time))
            this_time = 0 
    pg_matrix = np.full(max_cir,-1)
    tacc = 0
    for i in pgtxt:
        k = [m for m in range(len(i)) if i.startswith('=', m)]
        t = [m for m in range(len(i)) if i.startswith(' ', m)]
        time = float(i[k[-1]+1:len(i)])
        program = int(i[k[1]+1:t[2]])
        if time>0:
            tacc = tacc+time
        m = int(1/sample_t*tacc)
        pg_matrix[min(m,max_cir-1)] = program
    prog_matrix[chan_num.index(chan_sel)] = pg_matrix
    
    ctltxt = []
    this_time = 0    
    for i in ctrltxt:
        k = [m for m in range(len(i)) if i.startswith('=', m)]
        t = [m for m in range(len(i)) if i.startswith(' ', m)]
        channel = int(i[k[0]+1:t[1]])
        time = float(i[k[-1]+1:len(i)])
        if time>0:
            this_time = this_time+time
        if channel==chan_sel:
            ctltxt.append(i[0:k[-1]+1]+str(this_time))
            this_time = 0  
    ctl_matrix = np.full((2,max_cir),-1)
    tacc = 0
    for i in ctltxt:
        k = [m for m in range(len(i)) if i.startswith('=', m)]
        t = [m for m in range(len(i)) if i.startswith(' ', m)]
        time = float(i[k[-1]+1:len(i)])
        control = int(i[k[1]+1:t[2]])
        value = int(i[k[2]+1:t[3]])
        if time>0:
            tacc = tacc+time
        m = int(1/sample_t*tacc)
        ctl_matrix[0,min(m,max_cir-1)] = control
        ctl_matrix[1,min(m,max_cir-1)] = value
    ctrl_matrix[chan_num.index(chan_sel)] = ctl_matrix
    
    pchtxt = []
    this_time = 0    
    for i in pitchtxt:
        k = [m for m in range(len(i)) if i.startswith('=', m)]
        t = [m for m in range(len(i)) if i.startswith(' ', m)]
        channel = int(i[k[0]+1:t[1]])
        time = float(i[k[-1]+1:len(i)])
        if time>0:
            this_time = this_time+time
        if channel==chan_sel:
            pchtxt.append(i[0:k[-1]+1]+str(this_time))
            this_time = 0
    pch_matrix = np.full(max_cir,-1)
    tacc = 0
    for i in pchtxt:
        k = [m for m in range(len(i)) if i.startswith('=', m)]
        t = [m for m in range(len(i)) if i.startswith(' ', m)]
        time = float(i[k[-1]+1:len(i)])
        pitch = int(i[k[1]+1:t[2]])
        if time>0:
            tacc = tacc+time
        m = int(1/sample_t*tacc)
        pch_matrix[min(m,max_cir-1)] = pitch
    pitch_matrix[chan_num.index(chan_sel)] = pch_matrix
    
    afttxt = []
    this_time = 0    
    for i in aftchtxt:
        k = [m for m in range(len(i)) if i.startswith('=', m)]
        t = [m for m in range(len(i)) if i.startswith(' ', m)]
        channel = int(i[k[0]+1:t[1]])
        time = float(i[k[-1]+1:len(i)])
        if time>0:
            this_time = this_time+time
        if channel==chan_sel:
            afttxt.append(i[0:k[-1]+1]+str(this_time))
            this_time = 0  
    aft_matrix = np.full(max_cir,-1)
    tacc = 0
    for i in afttxt:
        k = [m for m in range(len(i)) if i.startswith('=', m)]
        t = [m for m in range(len(i)) if i.startswith(' ', m)]
        time = float(i[k[-1]+1:len(i)])
        value = int(i[k[1]+1:t[2]])
        if time>0:
            tacc = tacc+time
        m = int(1/sample_t*tacc)
        aft_matrix[min(m,max_cir-1)] = value
    aftch_matrix[chan_num.index(chan_sel)] = aft_matrix
    
    txt = []
    this_time = 0
    for i in notetxt:
        k = [m for m in range(len(i)) if i.startswith('=', m)]
        t = [m for m in range(len(i)) if i.startswith(' ', m)]
        channel = int(i[k[0]+1:t[1]])
        time = float(i[k[-1]+1:len(i)])
        note = int(i[k[1]+1:t[2]])
        if time>0:
            this_time = this_time+time
        if channel==chan_sel and note in note_name:
            txt.append(i[0:k[-1]+1]+str(this_time))
            this_time = 0
    
    note_data = []
    for i in txt:
        k = [m for m in range(len(i)) if i.startswith('=', m)]
        t = [m for m in range(len(i)) if i.startswith(' ', m)]
        note = int(i[k[1]+1:t[2]])
        if note not in note_data:
            note_data.append(note)
    note_data = list(sorted(note_data))
        
    # sort note data
    note_matrix = np.zeros((len(note_data),max_cir))
    tic = np.zeros((len(note_data),2))
    sequal = np.full((len(note_data),10000),-1)
    sequal_abs = np.full((len(note_data),5000),-1)
    tacc = 0
    for i in txt:
        k = [m for m in range(len(i)) if i.startswith('=', m)]    
        t = [m for m in range(len(i)) if i.startswith(' ', m)]
        note =int(i[k[1]+1:t[2]])
        velocity = int(i[k[2]+1:t[3]])
        time = float(i[k[-1]+1:len(i)])
        if time>0:
            tacc = tacc+time
        f = note_data.index(note)
        m = int(1/sample_t*tacc)
        if t[0]==7: # a new note is iserted
            if velocity>0: # a true insertion
                tic[f] = [m,velocity]
                sequal[f,np.where(sequal[f]==-1)[0][0]] = m
                sequal_abs[f,np.where(sequal_abs[f]==-1)[0][0]] = velocity
            else: # a note is finished
                note_matrix[f,int(tic[f,0]):m] = int(tic[f,1])
                sequal[f,np.where(sequal[f]==-1)[0][0]] = m-1            
        elif t[0]==8: # a note is finished
            note_matrix[f,int(tic[f,0]):m] = int(tic[f,1])
            sequal[f,np.where(sequal[f]==-1)[0][0]] = m-1  
        
    sequal2 = np.full((len(note_data),6000),-1)
    sequal_abs2 = np.full((len(note_data),6000),-1)
    for i in range(len(note_matrix)):
        tacc = 0
        for j in range(len(note_matrix[i])):       
            if tacc==0:
                sequal2[i,tacc] = j
                sequal_abs2[i,tacc] = int(note_matrix[i][j])  
                tacc+=1
            elif sequal_abs2[i,tacc-1]!=int(note_matrix[i][j]):
                sequal2[i,tacc] = j
                sequal_abs2[i,tacc] = int(note_matrix[i][j])  
                tacc+=1

    total_index[chan_sel] = note_data               
    total_note_matrix.append(note_matrix)
    total_sequal.append(sequal)
    total_sequal_abs.append(sequal_abs)
    total_sequal2.append(sequal2)
    total_sequal_abs2.append(sequal_abs2)  
    net_num = net_num+len(note_data)     
    
    for i in range(len(note_data)):
        ct = total_note_data.index(note_data[i])
        lap_note_matrix[ct] = lap_note_matrix[ct]+note_matrix[i]
        net_note_data.append([chan_sel,note_data[i]])

for i in range(len(lap_note_matrix)):
    tacc = 0
    for j in range(len(lap_note_matrix[i])):       
        if tacc==0:
            lap_sequal2[i,tacc] = j
            lap_sequal_abs2[i,tacc] = int(lap_note_matrix[i][j])  
            tacc+=1
        elif lap_sequal_abs2[i,tacc-1]!=int(lap_note_matrix[i][j]):
            lap_sequal2[i,tacc] = j
            lap_sequal_abs2[i,tacc] = int(lap_note_matrix[i][j])  
            tacc+=1    

net_note_matrix = np.zeros((net_num,max_cir))
pt = 0
for i in total_note_matrix:
    mt = len(i)
    net_note_matrix[pt:pt+mt] = i
    pt = pt+mt
    
coll_matrix = [prog_matrix,ctrl_matrix,pitch_matrix,aftch_matrix]
# ------------------------------------------------------------------ #  
# PLOT: input x is a list
# 0 - note wave
# 1 - wave amplitude/energy
# 2 - the TREE plot
# 3 - sub TREE plot
# 4 - the CD plot
# 5 - sub CD plot
# 6 - black CD plot
x = [2,4,6]
noteplot(x,song_name,max_cir,sample_t,chan_num,total_note_data,total_index,total_note_matrix,total_sequal,
         total_sequal_abs,total_sequal2,total_sequal_abs2,lap_note_matrix,lap_sequal2,lap_sequal_abs2)
# ------------------------------------------------------------------ #  



'''    
# transform
con_fact = np.zeros(512)
for i in range(512):
    con_fact[i] = np.sin(np.pi*i/512)

out_matrix = np.zeros((len(note_data),int(1/sample_t*songlen)))
for i in range(len(note_data)):
    out_matrix[i] = np.convolve(note_matrix[i],con_fact, 'same')
    t = np.amax(out_matrix[i])
    out_matrix[i] = np.round(out_matrix[i]/t*127)

out_matrix = note_matrix  
'''
# ------------------------------------------------------------------ # 
# EXPORT
outfilename = 'new_song.mid'
out_txt,out_midi = noteexport(net_num,net_note_data,net_note_matrix,coll_matrix,chan_num,max_cir,memFile.ticks_per_beat,sample_t)
out_midi.save(outfilename) 


