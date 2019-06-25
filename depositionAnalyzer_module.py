import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import *

def img_threshold(filename):
	img = cv.imread(filename,0)
	blur = cv.GaussianBlur(img,(5,5),0)
	ret3,bin_img = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
	#img = cv.medianBlur(img,5)
	#bin_img = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
	#        	cv.THRESH_BINARY,11,2)
	return bin_img

def imgL(img): #img lenght
	imgL = img.shape[0]
	return str(imgL)

def imgH(img): #img height
	imgH = img.shape[1]
	return str(imgH)

def imgsize(img): #img size in pixels
	size_image = img.shape[0]*img.shape[1]
	return 'pixels_'+str(size_image)

def nb_particles(img):   #number of particles (black pixels)
	wpxl = img.any(axis=-1).sum()
	size_image = img.shape[0]*img.shape[1]
	return size_image-wpxl

def bin_file(filename,image_bin): #create a file in B&W
	bin_filename = 'bin_'+filename
	cv.imwrite(bin_filename, image_bin)
	image = cv.imread(bin_filename)
	return image

def percentage(nb_particles,img): #percentage of particle in the image
	size_image = img.shape[0]*img.shape[1]
	percentage = nb_particles/size_image*100
	percentage=round(percentage,4)
	return percentage
