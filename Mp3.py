import tkinter.filedialog
from tkinter import * 
from PIL import ImageTk,Image
import pygame.mixer
from eyed3 import id3
import os
import cv2
import sqlite3

#SQL 

con=sqlite3.connect("Fav.db")
cur=con.cursor() 


#GLOBAL VARIABLES

tag = id3.Tag()
counter=0
song=0
vol=0
li=[]
for root, dirs, files in os.walk(r"C:\Users\Home\Music"):
    for file in files:
        if file.endswith(".mp3"):
             li.append(os.path.join(root, file))

si=[] 
for file in os.listdir(r"C:\Users\Home\Music"):
    if(file.endswith(".mp3")): 
        file=file.replace(".mp3","")
        si.append(file)

#TKINTER CONFIGURE

root = Tk()
root.config(bg="#ffffff")
root.geometry("610x350")
root.title("V2K AUDIO PLAYER")

#FUNCTIONS

def clear():
    Label(root,text="\t\t\t\t\t\t\t",bg="#ffffff").place(x=270,y=280)
    Label(root,text="\t\t\t\t\t\t\t",bg="#ffffff").place(x=270,y=300)
    Label(root,text="\t\t\t\t\t",bg="#ffffff").place(x=270,y=320) 

def play(): 
    clear()
    global song,vol
    if(song>=len(li)):
        song=0
    pygame.mixer.init() 
    pygame.mixer.music.load(li[song])
    pygame.mixer.music.play()
    tag.parse(li[song])
    vol=pygame.mixer.music.get_volume()
    img()
    volume=int(vol*100)+1
    Label(root,text="Title : "+tag.title,bg="#ffffff").place(x=270,y=280)
    Label(root,text="Artist : "+tag.artist,bg="#ffffff").place(x=270,y=300)
    Label(root,text="Album : "+tag.album,bg="#ffffff").place(x=270,y=320)
    Label(root,text="Volume : "+str(volume),bg="#ffffff").place(x=520,y=320)

def res(): 
    global counter 
    if (counter%2==0):
        Button(root,image=bt_play,command=res,relief=FLAT,bg="#ffffff").place(x=380,y=205) 
        pygame.mixer.music.pause()
        counter+=1
    else:
        Button(root,image=bt_pause,command=res,relief=FLAT,bg="#ffffff").place(x=380,y=205) 
        pygame.mixer.music.unpause()
        counter+=1


def after(): 
    global song
    song+=1
    play()

def before():  
    global song
    song-=1
    play()
 
def inc(): 
    global vol
    vol=pygame.mixer.music.get_volume()
    if(vol<1):
        vol=vol+0.1
        pygame.mixer.music.set_volume(vol)
    Label(root,text="\t\t",bg="#ffffff").place(x=520,y=320)
    Label(root,text="Volume : "+str(int(vol*100)+1),bg="#ffffff").place(x=520,y=320)


def dec(): 
    global vol
    vol=pygame.mixer.music.get_volume()
    if(vol>0):
        vol=vol-0.1
        pygame.mixer.music.set_volume(vol)
    Label(root,text="\t\t",bg="#ffffff").place(x=520,y=320)
    Label(root,text="Volume : "+str(int(vol*100)+1),bg="#ffffff").place(x=520,y=320)

def go1(): 
    cs=list_box.curselection()[0]
    selection=list_box.get(cs)
    global song,counter
    count=0
    for sub in li:
        if(sub.find(selection)>-1):
            song=count
            Button(root,image=bt_pause,command=res,relief=FLAT,bg="#ffffff").place(x=380,y=205)
            play()
        else:
            count+=1 

def go2(): 
    cs=list_box_my.curselection()[0]
    selection=list_box_my.get(cs)
    global song,counter
    count=0
    for sub in li:
        if(sub.find(selection)>-1):
            song=count
            Button(root,image=bt_pause,command=res,relief=FLAT,bg="#ffffff").place(x=380,y=205)
            play()
        else:
            count+=1
            


def img(): 
    with open(r'C:\Users\Home\Music\thumbnail.png','wb') as image:
        image.write(tag.images[0].image_data)
    img=cv2.imread(r'C:\Users\Home\Music\thumbnail.png')
    b,g,r=cv2.split(img)
    img=cv2.merge((r,g,b))
    im=Image.fromarray(img)
    im=im.resize((180,180))
    imgtk=ImageTk.PhotoImage(image=im)
    L=Label(root,image=imgtk)
    L.imgtk=imgtk
    L.place(x=325,y=15)

#SQL FUNCTIONS

def add_fav(): 
    cur.execute("insert into fav values(?,?)",(si[song],li[song]))
    con.commit()
    mylist()

def rem_fav(): 
    cur.execute("delete from fav where name=?",(si[song],))
    con.commit()
    mylist()

#LIST FUNCTIONS

def mylist():
    data=cur.execute("select name from fav") 
    list_box_my.delete(0,'end')
    for row in data.fetchall():
        list_box_my.insert(END,row[0])
    list_box_my.bind("<<ListboxSelect>>",lambda x:go2())
    list_box_my.place(x=10,y=200)

def allist():
    for item in si: 
        list_box.insert(END,item)
    list_box.bind("<<ListboxSelect>>",lambda x:go1())
    list_box.place(x=10,y=33)

play()

#IMAGES

bt_play = PhotoImage(file=r"D:\New\Project\play.png").subsample(8,8)
bt_pause = PhotoImage(file=r"D:\New\Project\pause.png").subsample(8,8)
bt_next = PhotoImage(file=r"D:\New\Project\next.png").subsample(7,7)
bt_prev = PhotoImage(file=r"D:\New\Project\prev.png").subsample(7,7)
bt_plus = PhotoImage(file=r"D:\New\Project\plus.png").subsample(15,15)
bt_minus = PhotoImage(file=r"D:\New\Project\minus.png").subsample(15,15)
bt_fav = PhotoImage(file=r"D:\New\Project\fav.png").subsample(10,10)   
bt_unfav = PhotoImage(file=r"D:\New\Project\unfav.png").subsample(10,10)  
#BUTTONS

Button(root,image=bt_pause,command=res,relief=FLAT,bg="#ffffff").place(x=380,y=205)
Button(root,image=bt_next,command=after,relief=FLAT,bg="#ffffff").place(x=450,y=200)
Button(root,image=bt_prev,command=before,relief=FLAT,bg="#ffffff").place(x=300,y=200)
Button(root,image=bt_plus,command=inc,relief=FLAT,bg="#ffffff").place(x=535,y=220) 
Button(root,image=bt_minus,command=dec,relief=FLAT,bg="#ffffff").place(x=260,y=220) 
Button(root,image=bt_fav,command=add_fav,relief=FLAT,bg="#ffffff").place(x=542,y=155)
Button(root,image=bt_unfav,command=rem_fav,relief=FLAT,bg="#ffffff").place(x=277,y=160)
#LABELS
Label(root,text="Add",bg="#ffffff").place(x=545,y=190)
Label(root,text="Remove",bg="#ffffff").place(x=270,y=190)

#LIST Labels

Label(root,text="My Songs ",relief=GROOVE,bg="#ffffff",bd=2).place(x=11,y=175)
Label(root,text="All Songs ",relief=GROOVE,bg="#ffffff",bd=2).place(x=11,y=8)

#LIST 


list_box_my = Listbox(root,relief=GROOVE,bg="#ffffff",bd=4,width=40,height=6)
mylist()
list_box = Listbox(root,relief=GROOVE,bg="#ffffff",bd=4,width=40,height=6)
allist()

#MAINLOOP
root.mainloop()

#CONNECTION CLOSE

con.close()