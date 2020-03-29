# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 15:49:01 2020

@author: ChenghaoAdmin
"""

import os
#import sys
def rename():
    
    count=1
    path='C:\\Users\\ChenghaoAdmin\\Desktop\\newdata'
    filelist=os.listdir(path)
    for files in filelist:
        Olddir=os.path.join(path,files)
        if os.path.isdir(Olddir):
            continue
        
        if count <10:
            Newdir=os.path.join(path,'0000'+str(count)+'.txt')
        elif count < 100:
            Newdir=os.path.join(path,'000'+str(count)+'.txt')
        elif count < 1000:
            Newdir=os.path.join(path,'00'+str(count)+'.txt')
        elif count < 10000:
            Newdir=os.path.join(path,'0'+str(count)+'.txt')
        
        os.rename(Olddir,Newdir)
        count+=1
    print("change"+str(count-1)+"files")

rename() 
