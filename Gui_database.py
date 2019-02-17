from Tkinter import *
import sqlite3
import cv2
import requests
import numpy as np
import os
from PIL import ImageTk,Image   
root = Tk()
root.geometry('760x500')
root.title("God'Eye")
canvas = Canvas(root, width =4500, height =1500)  
canvas.pack()  
img = ImageTk.PhotoImage(Image.open("C:/Python27/eye.png"))  
canvas.create_image(2, 20, anchor=NW, image=img)
global Id
id=StringVar()
Fullname=StringVar()
Age=StringVar()
c=StringVar()
Designation=StringVar()



def database():
   Id=id.get()
   name1=Fullname.get()
   age=Age.get()
   gender=c.get()
   designation=Designation.get()
   conn = sqlite3.connect('C:/Python27/SQLiteStudio/form.db')
   with conn:
      cursor=conn.cursor()
   cursor.execute('CREATE TABLE IF NOT EXISTS Student (id String,Fullname String, Age String,Gender String,Designation String)')
   cursor.execute('INSERT INTO Student (id,FullName,Age,Gender,Designation) VALUES(?,?,?,?,?)',(str(Id),str(name1),str(age),str(gender),str(designation)))
   conn.commit()
   return Id
   
   
             
label_0 = Label(root, text="God's Eye",width=20,font=("bold", 30),bg="black",fg="white")
label_0.place(x=90,y=53)

label_1 = Label(root, text="Your ID",width=10,font=("bold", 13),bg="black",fg="white")
label_1.place(x=80,y=100)
entry_1 = Entry(root,textvar=id,width=40)
entry_1.place(x=240,y=100)

label_2 = Label(root, text="Name",width=10,font=("bold", 13),bg="black",fg="white")
label_2.place(x=80,y=130)

entry_2 = Entry(root,textvar=Fullname,width=40)
entry_2.place(x=240,y=130)

label_3 = Label(root, text="Age",width=10,font=("bold", 13),bg="black",fg="white")
label_3.place(x=80,y=180)

entry_3 = Entry(root,textvar=Age,width=40)
entry_3.place(x=240,y=180)

label_4 = Label(root, text="Gender",width=10,font=("bold", 13),bg="black",fg="white")
label_4.place(x=80,y=280)

list1 = ['M','F'];

droplist=OptionMenu(root,c, *list1)
droplist.config(width=15,bg="orange")
c.set('Select your gender') 
droplist.place(x=240,y=280)

label_5 = Label(root, text="Designation",width=10,font=("bold", 13),bg="black",fg="white")
label_5.place(x=80,y=330)

entry_5 = Entry(root,textvar=Designation,width=40)
entry_5.place(x=240,y=330)
# for dataset
def image():
    Id = database()
    id = Id
    detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    sample = 0
    while True:
        req = requests.get('http://192.168.43.1:8080/shot.jpg')
        arr = np.asarray(bytearray(req.content), dtype=np.uint8)
        img = cv2.imdecode(arr, -1) # 'Load it as it is'
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            sample = sample + 1
            cv2.imwrite("dataSet3/user." + str(id) + '.' + str(sample) + ".jpg", gray[y:y + h, x:x + w])
            cv2.rectangle(img, (x, y), (x + w, y + h), (225, 0, 0), 2)
            cv2.waitKey(100)
        cv2.imshow('img', img)

        if (sample > 5):
            break
    cv2.destroyAllWindows()
    

Button(root, text='Submit ',width=20,bg='black',fg='white',command=database).place(x=180,y=380)
Button(root, text='Image Capture',width=20,bg='black',fg='white',command=image).place(x=450,y=380)

root.mainloop()
