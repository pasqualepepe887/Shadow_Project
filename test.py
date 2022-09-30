
from textwrap import fill
from tkinter import messagebox
import tkinter
import cv2 
import mediapipe as mp
import numpy as np
import time
import xlsxwriter
from mediapipe.framework.formats import landmark_pb2
import pyautogui
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import pandas as pd






interface= Tk()

interface.attributes('-zoomed', True)
interface.iconphoto(False, tkinter.PhotoImage(file='Icone.png'))

#app=FullScreenApp(interface)

#interface.geometry("800x500")
interface.update_idletasks()

w = interface.winfo_width()
h = interface.winfo_height()
interface.update_idletasks()
canvas = Canvas(interface, width=w, height=h,background = "#393434",bd = 0,highlightthickness=0,borderwidth=0)

interface.title("Shadow Project")

interface.configure(background = "#242121") 
img_ing= ImageTk.PhotoImage(Image.open("Load_Icone.png"))
button_img= ImageTk.PhotoImage(Image.open("button_img.png"))
button_img_prem= ImageTk.PhotoImage(Image.open("button_prem.png"))


a_rect = canvas.create_rectangle(15, 15, w-15,h-15 , fill = "#574F4F",outline="") # Spazio Avatar + Video
w2 = w/2 -10
w3 = w/2 +10
a_line = canvas.create_rectangle(w2, 15, w3,h-15 , fill = "#393434",outline="")
#load_image = canvas.create_image(w-w/4,h/2.5,image=img_ing)

w_avatar = w/2 -20
h_avatar = h-20
file_pos = ''

label =Label(interface,padx=0,pady=0,relief=FLAT, bg="#574F4F") #relief=FLAT, bg="#574F4F"
label.place(x=15, y=15)

label_video =Label(interface,padx=0,pady=0, bg="#574F4F") #Video
label_video.place(x=w-w/2.5, y=h/7)

label_video.configure(image=img_ing)
label_video.update_idletasks()
w_video=label_video.winfo_width()
h_video=label_video.winfo_height()

###canvas.pack()



fps_time = 0
#workbook = ''
#worksheet = ''
#f = ''
base_dati = (
    ['FPS', 'P.16(X)', 'P.14(X)', 'P.12(X)', 'P.11(X)', 'P.13(X)', 'P.15(X)','P.24(X)','P.23(X)','P.26(X)','P.25(X)','P.28(X)','P.27(X)','--','P.16(Y)', 'P.14(Y)', 'P.12(Y)', 'P.11(Y)', 'P.13(Y)', 'P.15(Y)','P.24(Y)','P.23(Y)','P.26(Y)','P.25(Y)','P.28(Y)','P.27(Y)',]
)

row = 0
col = 0

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

def load_item(total_item,rowt,colt):
  global workbook,worksheet
  for item in (total_item):
    worksheet.write(rowt, colt,     str(item))
    colt += 1

###load_item(base_dati,row,col)  

def button_do(event):


    global cap,file_pos,workbook,worksheet,base_dati
    file_pos= filedialog.askopenfilename()
    print(file_pos)
    if file_pos is None:
        messagebox.showinfo(title='Seleziona Un Video',message='Per Procedere Seleziona Un Video')
        return
    else:

        f = filedialog.asksaveasfile(mode='wb', defaultextension=".xlsx")
        workbook = xlsxwriter.Workbook(f)
        worksheet = workbook.add_worksheet()
        colt = 0
        for item in (base_dati):
             worksheet.write(0, colt,     item)
             colt += 1
        cap = cv2.VideoCapture(file_pos)
        show_frames()
        

def button_prem_rit(): #Torna all'immagine di defult
    global canvas
    canvas.itemconfig(button_load,image=button_img)

def motion_button(event): # quando il cursore va sopra al pulsante
    global canvas
    canvas.itemconfig(button_load,image=button_img_prem)
    canvas.after(500, button_prem_rit)

    


def show_frames():

        global file_pos,interface,row,col,fps_time,cap,h_avatar,w_avatar,label,label_video,worbook,worksheet,f


        label.place(x=15, y=15)
                               #Altezza         #Lunghezza
        sfondo = np.zeros((int(w_avatar+15),int(h_avatar-35),3), np.uint8) # Dimensioni Spazio Avatar
        sfondo[:,:] = [87, 79, 79] # Background Color

        with mp_pose.Pose(
             min_detection_confidence=0.8,
             min_tracking_confidence=0.5) as pose:


             success, image = cap.read()


             if not success:
                 print("Completato")
                 
                 messagebox.showinfo(title='Completato',message='Sincronizzazione Completata')
                 workbook.close()
                 #f.close()
                 return
      

                # interface.destroy()

            
             # Draw the pose annotation on the image.
             image.flags.writeable = True
             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
             results = pose.process(image)

             if results.pose_landmarks:
  
                mp_drawing.draw_landmarks(
                 image,
                 results.pose_landmarks,
                 mp_pose.POSE_CONNECTIONS,
                 landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
  
                
                lm = results.pose_landmarks

                center_coordinates = (int(lm.landmark[0].x*500),int(lm.landmark[0].y*500)) #Cordinate Punto 0

                sfondo = cv2.ellipse(sfondo, center_coordinates, (15, 20),0, 0, 360, (255,255,255),4)
                
                #__________Trapezio Corpo_________
                #12-11
                sfondo = cv2.line(sfondo,(int(lm.landmark[12].x*500),int(lm.landmark[12].y*500)),(int(lm.landmark[11].x*500),int(lm.landmark[11].y*500)),(255,255,255),4) 
                
                #12-24
                sfondo = cv2.line(sfondo,(int(lm.landmark[12].x*500),int(lm.landmark[12].y*500)),(int(lm.landmark[24].x*500),int(lm.landmark[24].y*500)),(255,255,255),4)
                
                #11-23
                sfondo = cv2.line(sfondo,(int(lm.landmark[11].x*500),int(lm.landmark[11].y*500)),(int(lm.landmark[23].x*500),int(lm.landmark[23].y*500)),(255,255,255),4)   
                
                #24-23
                sfondo = cv2.line(sfondo,(int(lm.landmark[24].x*500),int(lm.landmark[24].y*500)),(int(lm.landmark[23].x*500),int(lm.landmark[23].y*500)),(255,255,255),4)
                
                
                #________Braccia_____
                #12-14
                sfondo = cv2.line(sfondo,(int(lm.landmark[12].x*500),int(lm.landmark[12].y*500)),(int(lm.landmark[14].x*500),int(lm.landmark[14].y*500)),(255,255,255),4) 
                
                #14-16
                sfondo = cv2.line(sfondo,(int(lm.landmark[16].x*500),int(lm.landmark[16].y*500)),(int(lm.landmark[14].x*500),int(lm.landmark[14].y*500)),(255,255,255),4) 
                
                #11-13
                sfondo = cv2.line(sfondo,(int(lm.landmark[11].x*500),int(lm.landmark[11].y*500)),(int(lm.landmark[13].x*500),int(lm.landmark[13].y*500)),(255,255,255),4) 
                
                #13-15
                sfondo = cv2.line(sfondo,(int(lm.landmark[13].x*500),int(lm.landmark[13].y*500)),(int(lm.landmark[15].x*500),int(lm.landmark[15].y*500)),(255,255,255),4) 
                
                
                #_______Gambe________
                #24-26
                sfondo = cv2.line(sfondo,(int(lm.landmark[24].x*500),int(lm.landmark[24].y*500)),(int(lm.landmark[26].x*500),int(lm.landmark[26].y*500)),(255,255,255),4)
                
                #26-28
                sfondo = cv2.line(sfondo,(int(lm.landmark[26].x*500),int(lm.landmark[26].y*500)),(int(lm.landmark[28].x*500),int(lm.landmark[28].y*500)),(255,255,255),4)
                     
                #23-25
                sfondo = cv2.line(sfondo,(int(lm.landmark[23].x*500),int(lm.landmark[23].y*500)),(int(lm.landmark[25].x*500),int(lm.landmark[25].y*500)),(255,255,255),4)
                     
                #25-27
                sfondo = cv2.line(sfondo,(int(lm.landmark[25].x*500),int(lm.landmark[25].y*500)),(int(lm.landmark[27].x*500),int(lm.landmark[27].y*500)),(255,255,255),4)
                     
                
                
                #_____POINT_______
                sfondo = cv2.line(sfondo,(int(lm.landmark[12].x*500),int(lm.landmark[12].y*500)),(int(lm.landmark[12].x*500),int(lm.landmark[12].y*500)),(0,0,255),10) 
                sfondo = cv2.line(sfondo,(int(lm.landmark[11].x*500),int(lm.landmark[11].y*500)),(int(lm.landmark[11].x*500),int(lm.landmark[11].y*500)),(0,0,255),10) 
                sfondo = cv2.line(sfondo,(int(lm.landmark[24].x*500),int(lm.landmark[24].y*500)),(int(lm.landmark[24].x*500),int(lm.landmark[24].y*500)),(0,0,255),10) 
                sfondo = cv2.line(sfondo,(int(lm.landmark[23].x*500),int(lm.landmark[23].y*500)),(int(lm.landmark[23].x*500),int(lm.landmark[23].y*500)),(0,0,255),10) 
                sfondo = cv2.line(sfondo,(int(lm.landmark[0].x*500),int(lm.landmark[0].y*500)),(int(lm.landmark[0].x*500),int(lm.landmark[0].y*500)),(0,0,255),10) 
                sfondo = cv2.line(sfondo,(int(lm.landmark[14].x*500),int(lm.landmark[14].y*500)),(int(lm.landmark[14].x*500),int(lm.landmark[14].y*500)),(0,0,255),10) 
                sfondo = cv2.line(sfondo,(int(lm.landmark[16].x*500),int(lm.landmark[16].y*500)),(int(lm.landmark[16].x*500),int(lm.landmark[16].y*500)),(0,0,255),10) 
                sfondo = cv2.line(sfondo,(int(lm.landmark[13].x*500),int(lm.landmark[13].y*500)),(int(lm.landmark[13].x*500),int(lm.landmark[13].y*500)),(0,0,255),10) 
                sfondo = cv2.line(sfondo,(int(lm.landmark[15].x*500),int(lm.landmark[15].y*500)),(int(lm.landmark[15].x*500),int(lm.landmark[15].y*500)),(0,0,255),10) 
                sfondo = cv2.line(sfondo,(int(lm.landmark[26].x*500),int(lm.landmark[26].y*500)),(int(lm.landmark[26].x*500),int(lm.landmark[26].y*500)),(0,0,255),10) 
                sfondo = cv2.line(sfondo,(int(lm.landmark[28].x*500),int(lm.landmark[28].y*500)),(int(lm.landmark[28].x*500),int(lm.landmark[28].y*500)),(0,0,255),10) 
                sfondo = cv2.line(sfondo,(int(lm.landmark[25].x*500),int(lm.landmark[25].y*500)),(int(lm.landmark[25].x*500),int(lm.landmark[25].y*500)),(0,0,255),10) 
                sfondo = cv2.line(sfondo,(int(lm.landmark[27].x*500),int(lm.landmark[27].y*500)),(int(lm.landmark[27].x*500),int(lm.landmark[27].y*500)),(0,0,255),10) 
                  
              #resize
                #print(w_video,h_video)             
                image = cv2.resize(image, (w_video,h_video))  
                img_video = Image.fromarray(image)
    
                imgtk_video = ImageTk.PhotoImage(image = img_video)
                label_video.imgtk = imgtk_video
                label_video.configure(image=imgtk_video,borderwidth=10,relief="groove")
  
  
     
  
  
                #print(int(lm.landmark[16].x*500))
                fps_time+=1 
                row +=1
                dati = (
                [fps_time, int(lm.landmark[16].x*500), int(lm.landmark[14].x*500), int(lm.landmark[12].x*500), int(lm.landmark[11].x*500), int(lm.landmark[13].x*500), int(lm.landmark[16].x*500),int(lm.landmark[24].x*500),int(lm.landmark[23].x*500),int(lm.landmark[26].x*500),int(lm.landmark[25].x*500),int(lm.landmark[28].x*500),int(lm.landmark[27].x*500),'  ---  ',int(lm.landmark[16].y*500), int(lm.landmark[14].y*500), int(lm.landmark[12].y*500), int(lm.landmark[11].y*500), int(lm.landmark[13].y*500), int(lm.landmark[15].y*500),int(lm.landmark[24].y*500),int(lm.landmark[23].y*500),int(lm.landmark[26].y*500),int(lm.landmark[25].y*500),int(lm.landmark[28].y*500),int(lm.landmark[27].y*500)]
                )
                load_item(dati,row,col) 
  
         
                   
      


      
       # cv2image= cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        img = Image.fromarray(sfondo)
    
        imgtk = ImageTk.PhotoImage(image = img)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        label.after(1, show_frames)



imgtk = ImageTk.PhotoImage(Image.open("home_avatar.png"))
label.imgtk = imgtk
label.configure(image=imgtk)
label.place(x=w/6, y=h/3)

button_load = canvas.create_image(w-w/2.5,h/1.1, anchor=SW, image=button_img, state=NORMAL)

canvas.tag_bind(button_load, "<Button-1>", button_do)
canvas.tag_bind(button_load,'<Motion>',motion_button)


# <------
##button.place(x=25,y=100)
canvas.pack()
interface.mainloop()