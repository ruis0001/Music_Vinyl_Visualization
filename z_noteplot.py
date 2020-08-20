# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 22:34:14 2020

@author: Rui
"""

import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
from z_notelib import note_name,note_freq # read in note library

def noteplot(x,song_name,max_cir,sample_t,chan_num,total_note_data,total_index,total_note_matrix,total_sequal,
             total_sequal_abs,total_sequal2,total_sequal_abs2,lap_note_matrix,lap_sequal2,lap_sequal_abs2):
    song_name = song_name.replace('_', ' ')
    if 0 in x:  # note wave
        for tic in range(len(chan_num)):
            note_data = total_index[chan_num[tic]]
            note_matrix = total_note_matrix[tic]
        
            fig1, axs1 = plt.subplots(len(note_data),1,figsize=(24, 20))
            fig1.suptitle(song_name+',Channel:'+str(chan_num[tic]),fontsize = 20)
            for i in range(len(note_data)):
                if note_data[i] in note_name:
                    axs1[i].plot(note_matrix[i])
                    axs1[i].set_ylabel(note_name[note_data[i]])
                    

    if 1 in x:  # wave amplitude/energy
         for tic in range(len(chan_num)):
            note_data = total_index[chan_num[tic]]
            note_matrix = total_note_matrix[tic]
            
            #X = list(range(max_cir))
            Y = [0]*max_cir
            Z = [0]*max_cir
            for i in range(max_cir):
                for j in range(len(note_data)):
                    note_f = note_freq[note_data[j]]
                    velocityA = note_matrix[j,i]
                    note_m = velocityA/127*np.sin(2*np.pi*note_f*i*sample_t)
                    Y[i] = Y[i]+note_m
                    if velocityA>0:
                        Z[i] = Z[i]+note_f
            fig2, axs2 = plt.subplots(2,1,figsize=(24, 20))
            axs2[0].plot(Y)
            axs2[0].set_title(song_name+',Channel:'+str(chan_num[tic])+', aggregated amplitude',fontsize = 20)
            axs2[1].plot(Z)
            axs2[1].set_title(song_name+',Channel:'+str(chan_num[tic])+', aggregated energy',fontsize = 20)

    if 2 in x or 3 in x:  # the tree        
        total_trunk = 0
        if 2 in x:
            fig6, ax6 = plt.subplots(figsize=(24, 20))
            plt.gca().invert_yaxis()
            ax6.set_title(song_name,fontsize = 20)
        for tic in range(len(chan_num)):
            note_data = total_index[chan_num[tic]]
            note_matrix = total_note_matrix[tic]
            sequal = total_sequal[tic]
            sequal_abs = total_sequal_abs[tic]
            if 3 in x:
                fig3, ax3 = plt.subplots(figsize=(24, 20))
                fig3.suptitle(song_name+',Channel:'+str(chan_num[tic])+' - the Tree',fontsize = 20)
            trunk = 0
            for i in range(len(note_data)):
                temp_cir = []
                for t in sequal[i]:
                    if t!=-1:
                        temp_cir.append(int(t))
                    else:
                        break
                temp_cir_abs = []
                for t in sequal_abs[i]:
                    if t!=-1:
                        temp_cir_abs.append(int(t))
                    else:
                        break 
                
                note_f = note_freq[note_data[i]]    
                #light_s = 360/3.3*(10.8-np.log(note_f))
                #light_s = 360/2.3*(9.3-np.log(note_f))
                light_s = 360/4.15*(11.75-np.log(note_f))   #25-1600HZ
                
                if light_s<=740 and light_s>607:
                    rgbcolor = [1,(740-light_s)/(740-607),0]
                elif light_s<=607 and light_s>538:
                    rgbcolor = [(light_s-538)/(607-538),1,0]
                elif light_s<=538 and light_s>493:
                    rgbcolor = [0,1,(538-light_s)/(538-493)]
                elif light_s<=493 and light_s>468:
                    rgbcolor = [0,(light_s-468)/(493-468),1]
                elif light_s<=468 and light_s>=380:
                    rgbcolor = [0.5*(468-light_s)/(468-380),0,1]    
                
                aa0 = 0
                
                for t in range(len(temp_cir_abs)):   
                    if temp_cir[t*2+1]-temp_cir[t*2]>10:
                        x1 = np.arange(0,temp_cir_abs[t]*(temp_cir[t*2+1]-temp_cir[t*2]),100)
                        x2 = -np.delete(np.flip(x1),-1)
                        x1 = np.concatenate([x2,x1])
                        y1 = 1/temp_cir_abs[t]*x1+temp_cir[t*2]
                        for m in range(len(y1)-1):
                            y1[m] = y1[len(y1)-1-m]
                        y2 = temp_cir[t*2+1]
                        y3 = np.zeros(len(x1))
                        hs = int((len(x1)+1)/2)
                        for m in range(hs):
                            y3[hs-1+m] = temp_cir[t*2]+(temp_cir[t*2+1]-temp_cir[t*2])*np.sin(np.pi/2*m/hs)
                        y3[-1] = temp_cir[t*2+1]
                        for m in range(len(y3)-1):
                            y3[m] = y3[len(y3)-1-m]  
                        if t==0:
                            aa0 = temp_cir_abs[t]*(temp_cir[t*2+1]-temp_cir[t*2])/2
                            trunk = aa0/10
                        if t>0:
                            if x1[-1]/20<trunk:
                                trunk = x1[-1]/20
                            if (temp_cir[t*2]-temp_cir[t*2-1])==1:   # continuous note                
                                aa1 = x1[0:hs-1]-aa0
                                aa3 = x1[hs:len(x1)]+aa0
                                aa2 = np.arange(-aa0,aa0,100)
                                x1 = np.concatenate([aa1,aa2,aa3])
                                bb1 = y3[0:hs-1]
                                bb3 = y3[hs:len(y3)]
                                bb2 = np.full(len(aa2),temp_cir[t*2])
                                y3 = np.concatenate([bb1,bb2,bb3])
                                aa0 = x1[-1]/2
                            else:
                                aa0 = 0 
                        if 3 in x:
                            ax3.fill_between(x1,y3,y2,color = rgbcolor,alpha=0.3)
                        if 2 in x:
                            ax6.fill_between(x1,y3,y2,color = rgbcolor,alpha=0.3)
                total_trunk = max(total_trunk,trunk/4)
            if 3 in x:
                m1 = np.arange(-trunk,trunk,50)
                m2 = 0
                m3 = max_cir
                m4 = max_cir*1.25
                ax3.fill_between(m1,m2,m3, color = 'k',alpha=0.1)
                ax3.fill_between(m1,m3,m4, color = 'k',alpha=0.5)
                plt.gca().invert_yaxis()
        if 2 in x:
            m1 = np.arange(-total_trunk,total_trunk,50)
            m2 = 0
            m3 = max_cir
            m4 = max_cir*1.25
            ax6.fill_between(m1,m2,m3, color = 'k',alpha=0.1)
            ax6.fill_between(m1,m3,m4, color = 'k',alpha=0.5)
        
    
    if 4 in x or 5 in x:  # the cd
        width2 = 1/(len(total_note_data)+1)
        if 4 in x:
            fig5, ax5 = plt.subplots(figsize=(24, 20), subplot_kw=dict(aspect="equal"))
            ax5.set_title(song_name,fontsize = 20)

        for tic in range(len(chan_num)):
            note_data = total_index[chan_num[tic]]
            note_matrix = total_note_matrix[tic]
            sequal2 = total_sequal2[tic]
            sequal_abs2 = total_sequal_abs2[tic]
            
            if 5 in x:
                fig4, ax4 = plt.subplots(figsize=(24, 20), subplot_kw=dict(aspect="equal"))
                fig4.suptitle(song_name+',Channel:'+str(chan_num[tic])+' - the CD',fontsize = 20)

            width1 = 1/(len(note_data)+1)
            
            for i in range(len(note_data)):                
                temp_cir = []
                for t in sequal2[i]:
                    if t!=-1:
                        temp_cir.append(int(t))
                    else:
                        break
                data1 = []
                for j in range(len(temp_cir)-1):
                    data1.append(temp_cir[j+1]-temp_cir[j])
                if temp_cir[-1]<max_cir:
                    data1.append(max_cir-temp_cir[-1])
                
                temp_cir_abs = []
                for t in sequal_abs2[i]:
                    if t!=-1:
                        temp_cir_abs.append(int(t))
                    else:
                        break 
                temp_cir_abs[:] = [x/127 for x in temp_cir_abs]
                
                note_f = note_freq[note_data[i]]    
                #light_s = 360/3.3*(10.85-np.log(note_f))
                #light_s = 360/2.3*(9.3-np.log(note_f))
                light_s = 360/4.15*(11.75-np.log(note_f))   #25-1600HZ
                
                if light_s<=740 and light_s>607:
                    rgbcolor = [1,(740-light_s)/(740-607),0]
                elif light_s<=607 and light_s>538:
                    rgbcolor = [(light_s-538)/(607-538),1,0]
                elif light_s<=538 and light_s>493:
                    rgbcolor = [0,1,(538-light_s)/(538-493)]
                elif light_s<=493 and light_s>468:
                    rgbcolor = [0,(light_s-468)/(493-468),1]
                elif light_s<=468 and light_s>=380:
                    rgbcolor = [0.5*(468-light_s)/(468-380),0,1]    
                
                color1 = []
                for j in range(len(temp_cir_abs)):
                    color1.append(rgbcolor+[temp_cir_abs[j]])   
                
                if 5 in x:
                    wedges, texts = ax4.pie(data1, wedgeprops=dict(width=width1,ec='k',lw=0.1), radius = width1*(i+1), colors = color1)                
                if 4 in x:
                    tk = total_note_data.index(note_data[i])
                    wedges2, texts2 = ax5.pie(data1, wedgeprops=dict(width=width2,ec='k',lw=0.1), radius = width2*(tk+1), colors = color1)
        if 4 in x:
            fig5.savefig('plots/'+song_name+'_white.png')                
                    
    if 6 in x:
        width2 = 1/(len(total_note_data)+1)        
        fig6, ax6 = plt.subplots(figsize=(24, 20), subplot_kw=dict(aspect="equal"))
        ax6.set_title(song_name+', Vinyl',fontsize = 20)                
            
        for i in range(len(total_note_data)):                
            temp_cir = []
            for t in lap_sequal2[i]:
                if t!=-1:
                    temp_cir.append(int(t))
                else:
                    break
            data1 = []
            for j in range(len(temp_cir)-1):
                data1.append(temp_cir[j+1]-temp_cir[j])
            if temp_cir[-1]<max_cir:
                data1.append(max_cir-temp_cir[-1])
            
            temp_cir_abs = []
            for t in lap_sequal_abs2[i]:
                if t!=-1:
                    temp_cir_abs.append(int(t))
                else:
                    break 

            if max(temp_cir_abs)>0:
                temp_cir_abs[:] = [x/max(temp_cir_abs) for x in temp_cir_abs]
            
            note_f = note_freq[total_note_data[i]]    
            #light_s = 360/3.3*(10.85-np.log(note_f))
            #light_s = 360/2.3*(9.3-np.log(note_f))
            light_s = 360/4.15*(11.75-np.log(note_f))   #25-1600HZ
            
            if light_s<=740 and light_s>607:
                rgbcolor = [1,(740-light_s)/(740-607),0]
            elif light_s<=607 and light_s>538:
                rgbcolor = [(light_s-538)/(607-538),1,0]
            elif light_s<=538 and light_s>493:
                rgbcolor = [0,1,(538-light_s)/(538-493)]
            elif light_s<=493 and light_s>468:
                rgbcolor = [0,(light_s-468)/(493-468),1]
            elif light_s<=468 and light_s>=380:
                rgbcolor = [0.5*(468-light_s)/(468-380),0,1]    
            
            color1 = []
            for j in range(len(temp_cir_abs)):
                if temp_cir_abs[j]>0:
                    color1.append(rgbcolor+[temp_cir_abs[j]])
                else:
                    color1.append([0.,0.,0.,1])
                
            wedges3, texts3 = ax6.pie(data1, wedgeprops=dict(width=width2,ec='w',lw=0.1), radius = width2*(i+1), colors = color1)
        fig6.savefig('plots/'+song_name+'_vinyl.png')                 
                
                
                