import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import serial
import time
import math
import logging


root = tk.Tk()
# Get the screen width and height
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
req_screen_height = int(round((screen_height * 1)/3, 0))
root.geometry("%dx%d" % (screen_width, req_screen_height))

# Retrieve the logged data
first_full_data_list = []
second_full_data_list = []
third_full_data_list = []
with open('pit_data.log', 'r') as log_file:
    log_data = log_file.read()
    log_data = log_data.split("\n\n")
    #print(log_data[1])
    first_data_needed = 3   #**********change here to change graphed data*************
    for index in log_data:
        index = index.split(",")
        req_position = index[first_data_needed]
        req_position = req_position.split(":")
        req_data = req_position[1]
        req_data = req_data.split(".")
        req_data_decimalless = req_data[0]
        req_data_decimalless = int(req_data_decimalless)
        first_full_data_list.append(req_data_decimalless)
        
    second_data_needed = 4   #**********change here to change graphed data*************
    for index in log_data:
        index = index.split(",")
        req_position = index[second_data_needed]
        req_position = req_position.split(":")
        req_data = req_position[1]
        req_data = req_data.split(".")
        req_data_decimalless = req_data[0]
        req_data_decimalless = int(req_data_decimalless)
        second_full_data_list.append(req_data_decimalless)

    third_data_needed = 5   #**********change here to change graphed data*************
    for index in log_data:
        index = index.split(",")
        req_position = index[third_data_needed]
        req_position = req_position.split(":")
        req_data = req_position[1]
        req_data = req_data.split(".")
        req_data_decimalless = req_data[0]
        req_data_decimalless = int(req_data_decimalless)
        third_full_data_list.append(req_data_decimalless)

# # Create the canvas
req_canvas_width = 20*len(first_full_data_list)
# canvas = tk.Canvas(root, width=req_canvas_width, height=req_screen_height,bg="white")
# canvas.place(relx=1, rely=1, anchor="se")  
# Create a canvas with a horizontal scrollbar
canvas = tk.Canvas(root, width=req_canvas_width, height=req_screen_height, scrollregion=(0, 0, req_canvas_width, req_screen_height), bg='white')
hbar = tk.Scrollbar(root, orient=tk.HORIZONTAL)
hbar.pack(side=tk.BOTTOM, fill=tk.X)
hbar.config(command=canvas.xview)
canvas.config(xscrollcommand=hbar.set)
canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

# draw vertical lines
for i in range(len(first_full_data_list)):
    x = i * 20
    canvas.create_line(x, 0, x, 500, width=1, fill="gainsboro")
for i in range(30):
    y = i * 20
    canvas.create_line(0, y, len(first_full_data_list)* 20, y, width=1, fill="gainsboro")

# Function to plot graph
def plot_graph():

    first_data = first_full_data_list
    #canvas.delete("plot")
    # Get canvas size
    canvas_height = canvas.winfo_height()

    # Calculate x and y scaling factors
    x_scale = 20
    first_y_scale = canvas_height / max(first_data)
    # Plot data points
    for i in range(len(first_data)-1):
        x1 = i * x_scale
        y1 = canvas_height - first_data[i] * first_y_scale
        if i == len(first_data)-1:
            x2 = (i+2) * x_scale
        else:
            x2 = (i+1) * x_scale
        y2 = canvas_height - first_data[i+1] * first_y_scale
        canvas.create_line(x1, y1, x2, y2, tags="plot", fill="red", width=2)
        
        
    
    second_data = second_full_data_list
    # Calculate x and y scaling factors
    x_scale = 20
    second_y_scale = canvas_height / max(second_data)
    # Plot data points
    for i in range(len(second_data)-1):
        x1 = i * x_scale
        y1 = canvas_height - second_data[i] * second_y_scale
        if i == len(second_data)-1:
            x2 = (i+2) * x_scale
        else:
            x2 = (i+1) * x_scale
        y2 = canvas_height - second_data[i+1] * second_y_scale
        canvas.create_line(x1, y1, x2, y2, tags="plot", fill="green2", width=2)
        
    third_data = third_full_data_list
    # Calculate x and y scaling factors
    x_scale = 20
    second_y_scale = canvas_height / max(third_data)
    # Plot data points
    for i in range(len(third_data)-1):
        x1 = i * x_scale
        y1 = canvas_height - third_data[i] * second_y_scale
        if i == len(third_data)-1:
            x2 = (i+2) * x_scale
        else:
            x2 = (i+1) * x_scale
        y2 = canvas_height - third_data[i+1] * second_y_scale
        canvas.create_line(x1, y1, x2, y2, tags="plot", fill="purple", width=2)

plot_graph()
# Configure canvas to resize with window
canvas.bind("<Configure>", lambda event: plot_graph())


root.mainloop()