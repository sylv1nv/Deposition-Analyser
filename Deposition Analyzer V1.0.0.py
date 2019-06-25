#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import depositionAnalyzer_module as da
import os
import logging
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox, filedialog, Menu
from os import path #Handle file path
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from logging.handlers import RotatingFileHandler #log file


#Log system setup
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s :: %(message)s')
file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

def program_state(state):
    progressBar["value"] = state
    progressBar.update()

#Main function of Deposition Analyzer
def DA():
    filename=file.get()
    img_threshold = da.img_threshold(filename)
    logger.info("File_"+filename)
    program_state(20)
    image = da.bin_file(filename,img_threshold)
    logger.info('imgsize_'+da.imgH(image)+'x'+da.imgL(image))
    program_state(40)
    imgsize = da.imgsize(image)
    logger.info(imgsize)
    program_state(60)
    nbp = da.nb_particles(image)
    log_particle='particles_'+str(nbp)
    logger.info(log_particle)
    program_state(80)
    percent =  da.percentage(nbp,image)
    res.set(str(percent))
    program_state(100)
    log_percentage='percentage_'+str(percent)
    logger.info(log_percentage)

#About window
def About():
        messagebox.showinfo("About: Contact","GitHub: sylv1nv\nTwitter: @sylv1n_v\nVersion: 1.0.0\n\nMade with <3 by Sylvain V.")


#Help window
def help_window():
        help_window = Tk()
        help_window.title("Help")
        with open('about.txt', "r") as f:
                Label(help_window, text=f.read()).pack()
        help_window.mainloop()

#Take username function
def username():
        logger.info("--------------------")
        username = user.get()
        logger.info("User_"+username)

#View the log file directly in-app
def show_log():
    def getSize(filename):
        st = os.stat(filename)
        return st.st_size

    log_window = Tk()
    log_window.geometry("400x300")
    scrollbar = Scrollbar(log_window, orient="vertical")

    log_list = Listbox(log_window, width=50, height=20, yscrollcommand=scrollbar.set)
    log_list.config()
    scrollbar.config(command=log_list.yview)
    scrollbar.pack(side="right", fill="y")
    log_list.pack(side="left",fill="both", expand=True)

    file = open("activity.log","r")
    i=0
    for line in file:
        i=i+1
        log_list.insert(END,str(line))
    log_window.title('Logs '+str(i)+' entries - Size : '+str(getSize("activity.log"))+'Ko')

    log_window.mainloop()

#Compare Tool, compare the original image and the processed one
def compare_tool():
    alpha_slider_max = 100
    title_window = 'Image Comparator'
    src2_filename=file.get()
    src1_filename='bin_'+src2_filename

    if file.get() == '':
        messagebox.showinfo("Error","There is no image to compare")
        return
     

    def on_trackbar(val):
        alpha = val / alpha_slider_max
        beta = ( 1.0 - alpha )
        dst = cv.addWeighted(src1, alpha, src2, beta, 0.0)
        cv.imshow(title_window, dst)

    img1 = cv.imread(src1_filename)
    height, width = img1.shape[:2]
    src1 = cv.resize(img1,(int(width/2), int(height/2)), interpolation = cv.INTER_CUBIC)

    img2 = cv.imread(src2_filename)
    height, width = img2.shape[:2]
    src2 = cv.resize(img2,(int(width/2), int(height/2)), interpolation = cv.INTER_CUBIC)

    cv.namedWindow(title_window)
    trackbar_name = 'Alpha : '+str(alpha_slider_max)
    cv.createTrackbar(trackbar_name, title_window , 0, alpha_slider_max, on_trackbar)
    on_trackbar(0)
    cv.waitKey()



#Program window
window = Tk()
window.title("Deposition Analyzer")

#menu
menu_bar = Menu(window)

menu_file = Menu(menu_bar,tearoff=0)
menu_file.add_command(label="Logs",command=show_log)
menu_file.add_command(label="Quit",command=window.destroy)
menu_bar.add_cascade(label="File",menu=menu_file)

menu_image = Menu(menu_bar, tearoff=0)
menu_image.add_command(label="Compare",command=compare_tool)
menu_bar.add_cascade(label="Image",menu=menu_image)

menu_help = Menu(menu_bar,tearoff=0)
menu_help.add_cascade(label="Help", command=help_window)
menu_help.add_cascade(label="About",command=About)
menu_bar.add_cascade(label="Help", menu=menu_help)

window.config(menu=menu_bar)

tk.Label(window, justify='center', text ='Deposition Analizer', fg="black", font = "Verdana 15 bold").grid(row=1, columnspan=3)


#User Entry
user = StringVar()
Label(window, text ='User :').grid(row=2, sticky=E)
user = Entry(window, textvariable=user)
user.grid(row=2, column = 1)
user_btn = Button(window, text=("Enter"), command=username)
user_btn.grid(row=2, column=2)

#File Entry
file = StringVar()
Label(window, text ='Filename :').grid(row=3, sticky=E)
file = Entry(window, textvariable=file)
file.grid(row=3, column = 1)
btn = Button(window, text=("Enter"), command=DA)
btn.grid(row=3, column=2)

#Reult Entry
res = StringVar()
Label(window, text ='% :').grid(row=4, sticky=E)
result = Entry(window, state='disable', textvariable=res)
result.grid(row=4, column =1)
result.bind("<Return>", DA)

#programm running progress bar
progressBar = Progressbar(window, orient="horizontal", length=70, mode="determinate")
progressBar.grid(column=2, row=4, pady=5)


window.mainloop()
