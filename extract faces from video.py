from tkinter import *
import PIL
from PIL import Image, ImageGrab, ImageTk
import numpy as np
from tkinter import filedialog
import os.path
from os import path
import xlwt
from tkinter import messagebox
import cv2
from mtcnn.mtcnn import MTCNN
import os.path

vidcount = 0
detector = MTCNN()
#stares if it is in bulk or single file mode
state=0
source=""
destination=""


#assign where files will be saved
def assign_destination():
    global destination
    global name
    name = name_txt.get()
    dest_String = filedialog.askdirectory()
    destination = dest_String + "/extracted_" + name + "/"
    destination_lbl.configure(text=destination)

#assign the source video file
def assign_source():
    global source,state
    global file_list

    source = filedialog.askopenfilename(initialdir="/", title="Select file",
                                        filetypes=(("mp4", "*.mp4"), ("avi", "*.avi"), ("all files", "*.*")))
    state=0
    source_lbl.configure(text=source)
    bulk_lbl.configure(text="")


def assign_source_bulk():
    global source,state
    source = filedialog.askdirectory() + "/"
    state=1
    bulk_lbl.configure(text=source)
    source_lbl.configure(text="")

def start():
    global destination
    if not os.path.isdir(destination):
        os.mkdir(destination)
    if state==0:
        extract_single()
    elif state==1:
        extract_bulk()
    else:
        print("something went wrong with the state it is currently in ", str(state))

def extract_single():
    global source
    extract(source)


def extract_bulk():
    global source
    global vidcount
    file_list = os.listdir(source)
    length = len(file_list)
    for i in range(length):
        print("started with file number ",str(vidcount),":", str(file_list[i]))
        #extract(source + file_list[i])
        scaled_extract(source + file_list[i])
        print("finished with file:", str(file_list[i]))
        print("\n")


def extract(source):
    global name
    global vidcount
    name = name_txt.get()
    counter = 1
    limit = int(limit_txt.get())
    vidcap = cv2.VideoCapture(source)
    success, image = vidcap.read()
    count = 100000
    while success:
        ready = vidcap.read()
        pixels = image
        # detector = MTCNN()
        results = detector.detect_faces(pixels)
        if counter >= limit and len(results) != 0:
            print("confidence" + str(results[0]['confidence']))
            # cv2.imwrite(destination+"/"+name+"frame%d.jpg" % count, image)  # save frame as JPEG file
            # detect faces in the image

            # extract the bounding box from the first face
            # x1, y1, width, height = results[0]['box']

            x1, y1, width, height = results[0]['box']

            # x1=abs(x1)
            # y1=abs(y1)
            # width=abs(width)
            # height=abs(height)
            x2, y2 = x1 + width, y1 + height
            if y1 < 0:
                y1 = 0
                y2 = y2 + y1

            if x1 < 0:
                x1 = 0
                x2 = x2 + x1
            # extract the face
            face = pixels[y1:y2, x1:x2]
            # resize pixels to the model size
            image2 = Image.fromarray(face)
            image2 = image2.resize((224, 224))
            face_array = np.array(image2)
            # image2.save(destination+str(count)+".jpg")
            # cv2.imwrite(destination + "/" + name + str(vidcount) + "frame%d.jpg" % count, face_array)
            cv2.imwrite(destination + "/" + name + str(vidcount) + "frame%d.jpg" % count, face_array)
            counter = 1
            print('Read a new frame: ' + str(count), success, )
            count += 1
        counter = counter + 1
        success, image = vidcap.read()
    vidcount = vidcount + 1
    print("done")


def scaled_extract(source):
    global name
    global vidcount
    name = name_txt.get()
    counter = 1
    limit = int(limit_txt.get())
    vidcap = cv2.VideoCapture(source)
    success, image = vidcap.read()
    count = 100000
    while success:
        ready = vidcap.read()
        pixels = image
        img_shape = np.shape(pixels)
        height = img_shape[0]
        width = img_shape[1]
        xscale = width / 640
        yscale = height / 480
        temp_image = Image.fromarray(pixels)
        scaled_img = temp_image.resize((640, 480))
        scaled_img_arr=np.array(scaled_img)

        # detector = MTCNN()
        results = detector.detect_faces(scaled_img_arr)
        if counter >= limit and len(results) != 0:
            print("confidence" + str(results[0]['confidence']))
            # cv2.imwrite(destination+"/"+name+"frame%d.jpg" % count, image)  # save frame as JPEG file
            # detect faces in the image

            # extract the bounding box from the first face
            # x1, y1, width, height = results[0]['box']

            x1, y1, width, height = results[0]['box']

            # x1=abs(x1)
            # y1=abs(y1)
            # width=abs(width)
            # height=abs(height)
            x2, y2 = x1 + width, y1 + height
            if y1 < 0:
                y1 = 0
                y2 = y2 + y1

            if x1 < 0:
                x1 = 0
                x2 = x2 + x1
            # extract the face
            x1 = int(x1 * xscale)
            x2 = int(x2 * xscale)
            y1 = int(y1 * yscale)
            y2 = int(y2 * yscale)
            face = pixels[y1:y2, x1:x2]
            # resize pixels to the model size
            image2 = Image.fromarray(face)
            image2 = image2.resize((224, 224))
            face_array = np.array(image2)
            # image2.save(destination+str(count)+".jpg")
            # cv2.imwrite(destination + "/" + name + str(vidcount) + "frame%d.jpg" % count, face_array)
            cv2.imwrite(destination + "/" + name + str(vidcount) + "frame%d.jpg" % count, face_array)
            counter = 1
            print('Read a new frame: ' + str(count), success, )
            count += 1
        counter = counter + 1
        success, image = vidcap.read()
    vidcount = vidcount + 1
    print("done")


window = Tk()
window.title("frame extracting application")
window.geometry('750x750')
source = ""
destination = ""
name = ""

file_frame = Frame(master=window)
file_frame.grid(column=0, row=0)

destination_btn = Button(file_frame, text="destination", command=assign_destination)
destination_btn.grid(column=0, row=2,padx=5, pady=5)
destination_lbl = Label(file_frame, text=destination)
destination_lbl.grid(column=1, row=2)

name_lbl = Label(file_frame, text="Project Name")
name_lbl.grid(column=0, row=3)
name_txt = Entry(file_frame, width=25)
name_txt.grid(column=1, row=3)

start_btn = Button(file_frame, text="start", command=start)
start_btn.grid(column=0, row=5,padx=5, pady=5)

limit_txt = Entry(file_frame, text="entry")
limit_txt.grid(column=1, row=4)
limit_txt.insert(END,"0")
limit_lbl = Label(file_frame, text="skip frame")
limit_lbl.grid(column=0, row=4)

bulk_btn = Button(file_frame, text="bulk source", command=assign_source_bulk)
bulk_btn.grid(column=0, row=1,padx=5, pady=5)
bulk_lbl = Label(file_frame, text=source)
bulk_lbl.grid(column=1, row=1)


source_btn = Button(file_frame, text="source", command=assign_source)
source_btn.grid(column=0, row=0,padx=5, pady=5)
source_lbl = Label(file_frame, text=source)
source_lbl.grid(column=1, row=0)

window.mainloop()
