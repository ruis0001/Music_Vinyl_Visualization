# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 21:37:29 2020

@author: Rui
"""

note_name={21:'A0',22:'A#0/Bb0',23:'B0',24:'C1',25:'C#1/Db1',26:'D1',27:'D#1/Eb1',28:'E1',29:'F1',
           30:'F#1/Gb1',31:'G1',32:'G#1/Ab1',33:'A1',34:'A#1/Bb1',35:'B1',36:'C2',37:'C#2/Db2',
           38:'D2',39:'D#2/Eb2',40:'E2',41:'F2',42:'F#2/Gb2',43:'G2',44:'G#2/Ab2',45:'A2',46:'A#2/Bb2',
           47:'B2',48:'C3',49:'C#3/Db3',50:'D3',51:'D#3/Eb3',52:'E3',53:'F3',54:'F#3/Gb3',55:'G3',
           56:'G#3/Ab3',57:'A3',58:'A#3/Bb3',59:'B3',60:'C4',61:'C#4/Db4',62:'D4',63:'D#4/Eb4',64:'E4',
           65:'F4',66:'F#4/Gb4',67:'G4',68:'G#4/Ab4',69:'A4',70:'A#4/Bb4',71:'B4',72:'C5',73:'C#5/Db5',
           74:'D5',75:'D#5/Eb5',76:'E5',77:'F5',78:'F#5/Gb5',79:'G5',80:'G#5/Ab5',81:'A5',82:'A#5/Bb5',
           83:'B5',84:'C6',85:'C#6/Db6',86:'D6',87:'D#6/Eb6',88:'E6',89:'F6',90:'F#6/Gb6',91:'G6'}
           # ,
           #92:'G#6/Ab6',93:'A7',94:'A#7/Bb7',95:'B7',96:'C7',97:'C#7/Db7',98:'D7',99:'D#7/Eb7',
           #100:'E7',101:'F7',102:'F#7/Gb7',103:'G7',104:'G#7/Ab7',105:'A8',106:'A#8/Bb8',107:'B8'}
                     
note_freq={21:27.5,22:29.14,23:30.87,24:32.7,25:34.65,26:36.71,27:38.89,28:41.2,29:43.65,
           30:46.25,31:49.0,32:51.91,33:55.0,34:58.27,35:61.74,36:65.41,37:69.3,
           38:73.42,39:77.78,40:82.41,41:87.31,42:92.5,43:98.0,44:103.83,45:110.0,46:116.54,
           47:123.47,48:130.81,49:138.59,50:146.83,51:155.56,52:164.81,53:174.61,54:185.0,55:196.0,
           56:207.65,57:220.0,58:233.08,59:246.94,60:261.63,61:277.18,62:293.66,63:311.13,64:329.63,
           65:349.23,66:369.99,67:392.0,68:415.3,69:440.0,70:466.16,71:493.88,72:523.25,73:554.37,
           74:587.33,75:622.25,76:659.26,77:698.46,78:739.99,79:783.99,80:830.61,81:880.0,82:932.33,
           83:987.77,84:1046.5,85:1108.73,86:1174.66,87:1244.51,88:1318.51,89:1396.91,90:1479.98,91:1567.98}