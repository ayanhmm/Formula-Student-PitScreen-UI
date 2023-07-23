import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import serial
import time
import math
import logging

#----------------------------------------------Configure logging----------------------------------------------
#logging.basicConfig(filename='pit_data.log', level=logging.INFO, format='\n%(asctime)s, %(message)s')


# ----------------------------------------------Create the root window----------------------------------------------
root = tk.Tk()
root.configure(bg="black")
root.title("TDR - SDC")


#----------------------------------------------bg of root window----------------------------------------------
# Get the screen width and height
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
# screen_height = int(round((screen_height*2)/7, 0))
# screen_width = int(round((screen_width*5)/15, 0))
#print(screen_width, screen_height)
actual_screen_height = screen_height
screen_height = int(round((actual_screen_height * 28)/30, 0))

root.geometry("%dx%d" % (screen_width, screen_height))

#make bg dimentions equal to window 
bg_image_pg1 = Image.open("pit display.png")
if bg_image_pg1.size != (screen_width, screen_height):
    # bg_image_pg1 = bg_image_pg1.resize((screen_width, screen_height), Image.ANTIALIAS) 
    # antialias method is removed in pillow 10 on july 2023
    bg_image_pg1 = bg_image_pg1.resize((screen_width, screen_height), Image.Resampling.LANCZOS) 
bg_image_pg1 = ImageTk.PhotoImage(bg_image_pg1)

##Adding background image in form of a label
##removed since adding blinking caution button is easiar in canvas
# bg_label_pg1 = ttk.Label(root, image = bg_image_pg1)
# bg_label_pg1.place(relx=0, rely=0, anchor="nw")
# bg_label_pg1.image = bg_image_pg1

#Adding background image in form of a canvas
bg_canvas_pg1 = tk.Canvas(root, width=screen_width, height=screen_height,bg="red")
bg_canvas_pg1.place(relx=1, y=actual_screen_height+10, anchor="se")
bg_canvas_pg1.create_image(0, 0, anchor="nw", image=bg_image_pg1)


root.attributes('-fullscreen', True)

#----------------------------------------------make canvas for throttle bar----------------------------------------------
throttle_canvas = tk.Canvas(root, width=int(round((screen_width * 27)/36, 0)), height=int(round((screen_height * 1)/20, 0)),bg="black", borderwidth=0, highlightthickness=0)
throttle_canvas.place(relx=-0.05, y=int(round((actual_screen_height * 1)/60, 0)), anchor="nw")

throttle_canvas_outer_outline_rectangle = throttle_canvas.create_rectangle(int(round((screen_width * 4)/36, 0)), 0, int(round((screen_width * 23)/36, 0)), int(round((screen_height * 1)/20, 0)),fill="Orange Red", outline="white",width="2", tags="throttle_outline")
throttle_canvas_inner_outline_rectangle = throttle_canvas.create_rectangle(int(round((screen_width * 9)/72, 0)), 0, int(round((screen_width * 45)/72, 0)), int(round((screen_height * 1)/20, 0)),fill="black", outline="white",width="2", tags="throttle_outline")

throttle_bar_outline_rectangle = throttle_canvas.create_rectangle(int(round((screen_width * 9)/38, 0)), int(round((screen_height * 1)/100, 0)), int(round((screen_width * 43)/72, 0)), int(round((screen_height * 8)/200, 0)),fill="black", outline="white",width="1", tags="throttle_outline")

throttle_canvas.create_text(int(round((screen_width * 16)/72, 0)), int(round((screen_height * 1)/68, 0)), text="THROTTLE ::", font=("areal black", int(round((screen_height * 1)/46, 0))), fill="white",anchor="ne" )

def create_gradient_throttle(current, total):
            speedometer_bg_outer_gradient_colour = (255,165,0)    # Start color (red)
            speedometer_bg_inner_gradient_colour = (200,0,0) 
            r1, g1, b1 = speedometer_bg_outer_gradient_colour
            r2, g2, b2 = speedometer_bg_inner_gradient_colour

            r = int(r1 + ((r2-r1) * current/total))
            g = int(g1 + ((g2-g1) * current/total))
            b = int(b1 + ((b2-b1) * current/total))

            return "#%02x%02x%02x" % (r, g, b)
        
for i in range(100):
    gradient_color = create_gradient_throttle(100-i,100)
    throttle_canvas.create_rectangle(int(round((screen_width * 64800)/273600, 0))+1, int(round((screen_height * 2)/200, 0))+1, int(round((screen_width * (((100-i)*986)+64800))/273600, 0))-1, int(round((screen_height * 1)/25, 0))-1,fill=gradient_color, outline=gradient_color ,width="1", tags="throttle_outline")
#----------------------------------------------CREATE DATA DISPLAY LABELS for circular display----------------------------------------------
# Create label to display pack VOLTAGE
display_labels_font_style = "RACE SPACE REGULAR"
circular_display_labels_font_color = "Orange Red"
list_display_labels_font_color = "Orange Red"

label_data_pack_voltage = tk.Label(bg_canvas_pg1, text="BV", font=(display_labels_font_style, int(round((screen_width * 1)/45, 0))), bg="black", fg=circular_display_labels_font_color)
label_data_pack_voltage.place(relx=0.065, rely=0.1026, anchor="center")

# Create label to display throttle
label_data_throttle = tk.Label(bg_canvas_pg1, text="AT", font=(display_labels_font_style, int(round((screen_width * 1)/45, 0))), bg="black", fg=circular_display_labels_font_color)
label_data_throttle.place(relx=0.35, rely=0.1026, anchor="center")
# Create label to display pack CURRENT
label_data_pack_current = tk.Label(bg_canvas_pg1, text="BC", font=(display_labels_font_style, int(round((screen_width * 1)/45, 0))), bg="black", fg=circular_display_labels_font_color)
label_data_pack_current.place(relx=0.215, rely=0.1026, anchor="center")

# Create label to display MOTOR TEMP
label_data_motor_temperature = tk.Label(bg_canvas_pg1, text="MT", font=(display_labels_font_style, int(round((screen_width * 1)/45, 0))), bg="black", fg=circular_display_labels_font_color)
label_data_motor_temperature.place(relx=0.59, rely=0.1026, anchor="center")
# Create label to display MOTOR controller TEMP
label_data_motor_controller_temperature = tk.Label(bg_canvas_pg1, text="MCT", font=(display_labels_font_style, int(round((screen_width * 1)/45, 0))), bg="black", fg=circular_display_labels_font_color)
label_data_motor_controller_temperature.place(relx=0.47, rely=0.1026, anchor="center")

#----------------------------------------------CREATE DATA DISPLAY LABELS for list display----------------------------------------------
# Create label to display charge
label_data_charge = tk.Label(bg_canvas_pg1, text="crg", font=(display_labels_font_style, int(round((screen_width * 1)/60, 0))), bg="black", fg=list_display_labels_font_color)
label_data_charge.place(relx=0.5, rely=0.350, anchor="center")
# Create label to display battery_max_temperature
label_data_battery_max_temperature = tk.Label(bg_canvas_pg1, text="maxt", font=(display_labels_font_style, int(round((screen_width * 1)/60, 0))), bg="black", fg=list_display_labels_font_color)
label_data_battery_max_temperature.place(relx=0.59, rely=0.417, anchor="center")

# Create label to display mfr
label_data_mfr = tk.Label(bg_canvas_pg1, text="mfr", font=(display_labels_font_style, int(round((screen_width * 1)/60, 0))), bg="black", fg=list_display_labels_font_color)
label_data_mfr.place(relx=0.46, rely=0.300, anchor="center")
# Create label to display battery_min_temperature
label_data_battery_min_temperature = tk.Label(bg_canvas_pg1, text="mint", font=(display_labels_font_style, int(round((screen_width * 1)/60, 0))), bg="black", fg=list_display_labels_font_color)
label_data_battery_min_temperature.place(relx=0.6, rely=0.48, anchor="center")
# Create label to display BPS
label_data_bps = tk.Label(bg_canvas_pg1, text="bps", font=(display_labels_font_style, int(round((screen_width * 1)/60, 0))), bg="black", fg=list_display_labels_font_color)
label_data_bps.place(relx=0.47, rely=0.537, anchor="center")  

# Create label to display AC CURRENT
label_data_AC_current = tk.Label(bg_canvas_pg1, text="AC", font=(display_labels_font_style, int(round((screen_width * 1)/60, 0))), bg="black", fg=list_display_labels_font_color)
label_data_AC_current.place(relx=0.537, rely=0.59, anchor="center")  
# Create label to display DC CURRENT
label_data_DC_current = tk.Label(bg_canvas_pg1, text="DC", font=(display_labels_font_style, int(round((screen_width * 1)/60, 0))), bg="black", fg=list_display_labels_font_color)
label_data_DC_current.place(relx=0.545, rely=0.658, anchor="center")  
#----------------------------------------------CREATE Fault DISPLAY LABELS----------------------------------------------
# # Create label to display MOTOR controller faults
# label_data_motor_controller_fault = tk.Label(bg_canvas_pg1, text="FAULT", font=(display_labels_font_style, 20), bg="black", fg="red")
# label_data_motor_controller_fault.place(relx=0.1, rely=0.76, anchor="nw")
# # Create label to display bms faults
# #label_data_bms_fault = tk.Label(root, text="FAULT", font=(20), bg="black", fg="red", width=80 , wraplength=800 ) #this is text wraping which is not working at the moment
# label_data_bms_fault = tk.Label(bg_canvas_pg1, text="FAULT", font=(display_labels_font_style, 20), bg="black", fg="red" )
# label_data_bms_fault.place(relx=0.1, rely=0.4, anchor="nw")
# Create label to display all faults
label_data_all_faults = tk.Label(bg_canvas_pg1, text="FAULT", font=(display_labels_font_style,  int(round((screen_width * 1)/45, 0))), bg="black", fg="red")
label_data_all_faults.place(relx=0.03, rely=0.33, anchor="nw")
#----------------------------------------------CREATE RPM and speed DISPLAY LABELS----------------------------------------------
#become obsolete after addition of speedometer and rpm dial
# # Create label to display RPM
# label_data_rpm = tk.Label(root, text="RPM", font=("Arial black", 15), bg="black", fg="red")
# label_data_rpm.place(relx=0.42, rely=0.43, anchor="center")
# # Create label to display speed
# label_data_speed = tk.Label(root, text="SPD", font=("Arial black", 20), bg="black", fg="red")
# label_data_speed.place(relx=0.57, rely=0.41, anchor="center")

#----------------------------------------------CREATE fault header text----------------------------------------------
faults_header_text = bg_canvas_pg1.create_text(int(round((screen_width * 1)/7, 0)), int(round((screen_height * 2)/7, 0)), text="! FAULTS !", font=("caution", int(round((screen_height)/11, 0))), fill='orange', state='normal')
global faults_header_text_disappearence_counter 
faults_header_text_disappearence_counter = 0

#----------------------------------------------make canvas' to display graphs----------------------------------------------
graph_1_canvas = tk.Canvas(root, width=int(round((screen_width * 1)/3, 0)), height=int(round((screen_height * 1)/3, 0)),bg="black")
graph_1_canvas.place(relx=1, rely=0, anchor="ne")
graph_1_canvas.create_text(int(round((screen_width * 1)/6, 0)), int(round((screen_height * 1)/45, 0)), text="MOTOR TEMPERATURE GRAPH", font=("areal black", int(round((screen_height * 1)/46, 0))), fill="white")
# draw vertical lines
for i in range(int(round((screen_width * 1)/3, 0))):
    x = i * int(round((screen_height * 1)/45, 0))
    graph_1_canvas.create_line(x, int(round((screen_width * 1)/36, 0)), x, int(round((screen_width * 1), 0)), width=1, fill="LightGoldenrod4")
# draw horizontal lines
for i in range(int(round((screen_height * 1)/3, 0))):
    if i != 1:
        y = i * int(round((screen_height * 1)/45, 0))
        graph_1_canvas.create_line(0, y, int(round((screen_height * 1), 0)), y, width=1, fill="LightGoldenrod4")


graph_2_canvas = tk.Canvas(root, width=int(round((screen_width * 1)/3, 0)), height=int(round((screen_height * 1)/3, 0)),bg="black")
graph_2_canvas.place(relx=1, rely=0.33, anchor="ne")
graph_2_canvas.create_text(int(round((screen_width * 1)/6, 0)), int(round((screen_height * 1)/45, 0)), text="RPM GRAPH", font=("areal black", int(round((screen_height * 1)/46, 0))), fill="white")
# draw vertical lines
for i in range(int(round((screen_width * 1)/3, 0))):
    x = i * int(round((screen_height * 1)/45, 0))
    graph_2_canvas.create_line(x, int(round((screen_width * 1)/36, 0)), x, int(round((screen_width * 1), 0)), width=1, fill="LightGoldenrod4")
# draw horizontal lines
for i in range(int(round((screen_height * 1)/3, 0))):
    if i != 1:
        y = i * int(round((screen_height * 1)/45, 0))
        graph_2_canvas.create_line(0, y,  int(round((screen_height * 1), 0)), y, width=1, fill="LightGoldenrod4")

graph_3_canvas = tk.Canvas(root, width=int(round((screen_width * 1)/3, 0)), height=int(round((screen_height * 1)/3, 0)),bg="black")
graph_3_canvas.place(relx=1, rely=1, anchor="se")
graph_3_canvas.create_text(int(round((screen_width * 1)/6, 0)), int(round((screen_height * 1)/45, 0)), text="SPEED GRAPH", font=("areal black", int(round((screen_height * 1)/46, 0))), fill="white")
# draw vertical lines
for i in range(int(round((screen_width * 1)/3, 0))):
    x = i * int(round((screen_height * 1)/45, 0))
    graph_3_canvas.create_line(x, int(round((screen_width * 1)/36, 0)), x, int(round((screen_width * 1), 0)), width=1, fill="LightGoldenrod4")
# draw horizontal lines
for i in range(int(round((screen_height * 1)/3, 0))):
    if i != 1:
        y = i * int(round((screen_height * 1)/45, 0))
        graph_3_canvas.create_line(0, y,  int(round((screen_height * 1), 0)), y, width=1, fill="LightGoldenrod4")


#----------------------------------------------make list of graph data to prevent errors in update_data function ----------------------------------------------
plot_1_data = [0,5,3,2,8,1]
plot_2_data = [0,5,3,2,8,1]
plot_3_data = [0,5,3,2,8,1]

#----------------------------------------------make canvas for speedometer and rpm----------------------------------------------
speedometer_canvas_height = int(round((screen_height * 1)/4, 0))
speedometer_canvas_width = (speedometer_canvas_height - int(round((screen_height * 1)/22.5, 0)))*2
speedometer_canvas = tk.Canvas(root, width=speedometer_canvas_width, height=speedometer_canvas_height, bg="black", borderwidth=0, highlightthickness=0)
#speedometer_canvas.place(relx=0.66, rely=1, anchor="se")
speedometer_canvas.place(x=((screen_width*2)/3)-(speedometer_canvas_width/2)-10, rely=1, anchor="se")
speedometer_canvas.create_text(speedometer_canvas_width/2, speedometer_canvas_height - int(round((screen_height * 1)/45, 0)), text="SPEED", font=("areal black", int(round((screen_height * 1)/46, 0))), fill="white")

rpm_canvas_width = int(round(speedometer_canvas_width/2, 0))
rpm_canvas_height = speedometer_canvas_height
rpm_dial_canvas = tk.Canvas(root, width=speedometer_canvas_width/2, height=speedometer_canvas_height, bg="black", borderwidth=0, highlightthickness=0)
#rpm_dial_canvas.place(x=((screen_width*2)/3)-speedometer_canvas_width-10, rely=1, anchor="se")
rpm_dial_canvas.place(relx=0.66, rely=1, anchor="se")
rpm_dial_canvas.create_text(rpm_canvas_width/2, rpm_canvas_height- int(round((screen_height * 1)/45, 0)), text="RPM", font=("areal black", int(round((screen_height * 1)/46, 0))), fill="white")

#----------------------------------------------make speedometer bg on the canvas----------------------------------------------
speedometer_radius = int(speedometer_canvas_width/2)

speedometer_canvas.create_arc(0, 0, 2*speedometer_radius, 2*speedometer_radius, fill="white", start=10, extent=10, outline="black",width="0.2", tags="speedometer_dial_outline_fill")
speedometer_canvas.create_arc(0, 0, 2*speedometer_radius, 2*speedometer_radius, fill="white", start=30, extent=10, outline="black",width="0.5", tags="speedometer_dial_outline_fill")
speedometer_canvas.create_arc(0, 0, 2*speedometer_radius, 2*speedometer_radius, fill="white", start=50, extent=10, outline="black",width="0.5", tags="speedometer_dial_outline_fill")
speedometer_canvas.create_arc(0, 0, 2*speedometer_radius, 2*speedometer_radius, fill="white", start=70, extent=10, outline="black",width="0.5", tags="speedometer_dial_outline_fill")
speedometer_canvas.create_arc(0, 0, 2*speedometer_radius, 2*speedometer_radius, fill="white", start=90, extent=10, outline="black",width="0.5", tags="speedometer_dial_outline_fill")
speedometer_canvas.create_arc(0, 0, 2*speedometer_radius, 2*speedometer_radius, fill="white", start=110, extent=10, outline="black",width="0.5", tags="speedometer_dial_outline_fill")
speedometer_canvas.create_arc(0, 0, 2*speedometer_radius, 2*speedometer_radius, fill="white", start=130, extent=10, outline="black",width="0.5", tags="speedometer_dial_outline_fill")
speedometer_canvas.create_arc(0, 0, 2*speedometer_radius, 2*speedometer_radius, fill="white", start=150, extent=10, outline="black",width="0.5", tags="speedometer_dial_outline_fill")
speedometer_canvas.create_arc(0, 0, 2*speedometer_radius, 2*speedometer_radius, fill="white", start=170, extent=10, outline="black",width="0.5", tags="speedometer_dial_outline_fill")

def create_gradient(current, total):
            speedometer_bg_outer_gradient_colour = (200,200,200)    # Start color (red)
            speedometer_bg_inner_gradient_colour = (50,50,50) 
            r1, g1, b1 = speedometer_bg_outer_gradient_colour
            r2, g2, b2 = speedometer_bg_inner_gradient_colour

            r = int(r1 + (r2-r1) * current/total)
            g = int(g1 + (g2-g1) * current/total)
            b = int(b1 + (b2-b1) * current/total)

            return "#%02x%02x%02x" % (r, g, b)
for i in range(speedometer_radius-int(round((screen_height * 1)/80, 0))):
    gradient_color = create_gradient(i,speedometer_radius)
    speedometer_canvas.create_arc(i+int(round((screen_height * 1)/80, 0)), i+int(round((screen_height * 1)/80, 0)), (2*speedometer_radius)-i-int(round((screen_height * 1)/80, 0)), (2*speedometer_radius)-i-int(round((screen_height * 1)/80, 0)), fill=gradient_color, start=0, extent=180, outline="",width="3", tags="speedometer_dial_gradient")

speedometer_canvas.create_arc(0, 0, 2*speedometer_radius, 2*speedometer_radius, fill="", start=0, extent=180, outline="gray30",width="3", tags="speedometer_dial_outline_outer")
speedometer_canvas.create_arc(int(round((screen_height * 1)/80, 0)), int(round((screen_height * 1)/80, 0)), 2*speedometer_radius-int(round((screen_height * 1)/80, 0)), 2*speedometer_radius-int(round((screen_height * 1)/80, 0)), fill="", start=0, extent=180, outline="gray30",width="3", tags="speedometer_dial_outline_inner")

speedometer_circle_center_x = speedometer_radius
speedometer_circle_center_y = speedometer_radius
speed_list = "5 10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 85"
speed_list = speed_list.split(" ")
angle = 170
speedometer_text_radius = speedometer_radius - int(round((screen_height * 1)/40, 0))  # Distance between the arc and the text
for char in speed_list:
    x = speedometer_circle_center_x + speedometer_text_radius * math.cos(math.radians(angle))
    y = speedometer_circle_center_y - speedometer_text_radius * math.sin(math.radians(angle))
    angle = angle-10
    speedometer_canvas.create_text(x, y, text=char, font=("Arial", int(round((screen_height * 1)/60, 0))), fill="black")


#----------------------------------------------make rpm bg on the canvas----------------------------------------------
rpm_dial_radius = int(rpm_canvas_width)

rpm_dial_canvas.create_arc(0, 0, 2*rpm_dial_radius, 2*rpm_dial_radius, fill="white", start=90, extent=10, outline="black",width="0.5", tags="rpm_dial_outline_fill")
rpm_dial_canvas.create_arc(0, 0, 2*rpm_dial_radius, 2*rpm_dial_radius, fill="white", start=110, extent=10, outline="black",width="0.5", tags="rpm_dial_outline_fill")
rpm_dial_canvas.create_arc(0, 0, 2*rpm_dial_radius, 2*rpm_dial_radius, fill="white", start=130, extent=10, outline="black",width="0.5", tags="rpm_dial_outline_fill")
rpm_dial_canvas.create_arc(0, 0, 2*rpm_dial_radius, 2*rpm_dial_radius, fill="white", start=150, extent=10, outline="black",width="0.5", tags="rpm_dial_outline_fill")
rpm_dial_canvas.create_arc(0, 0, 2*rpm_dial_radius, 2*rpm_dial_radius, fill="white", start=170, extent=10, outline="black",width="0.5", tags="rpm_dial_outline_fill")

for i in range(rpm_dial_radius-int(round((screen_height * 1)/90, 0))):
    gradient_color = create_gradient(i,rpm_dial_radius)
    rpm_dial_canvas.create_arc(i+int(round((screen_height * 1)/80, 0)), i+int(round((screen_height * 1)/80, 0)), (2*rpm_dial_radius)-i-int(round((screen_height * 1)/80, 0)), (2*rpm_dial_radius)-i-int(round((screen_height * 1)/80, 0)), fill=gradient_color, start=90, extent=90, outline="",width="3", tags="rpm_dial_gradient")

rpm_dial_canvas.create_arc(0, 0, 2*rpm_dial_radius, 2*rpm_dial_radius, fill="", start=90, extent=90, outline="gray30",width="3", tags="rpm_dial_outline_outer")
rpm_dial_canvas.create_arc(int(round((screen_height * 1)/80, 0)), int(round((screen_height * 1)/80, 0)), 2*rpm_dial_radius-int(round((screen_height * 1)/80, 0)), 2*rpm_dial_radius-int(round((screen_height * 1)/80, 0)), fill="", start=90, extent=90, outline="gray30",width="3", tags="rpm_dial_outline_inner")

rpm_dial_circle_center_x = rpm_dial_radius
rpm_dial_circle_center_y = rpm_dial_radius
rpm_list = "1 2 3 4 5 6 7 8"
rpm_list = rpm_list.split(" ")
angle = 170
text_radius = rpm_dial_radius - int(round((screen_height * 1)/40, 0))  # Distance between the arc and the text
for char in rpm_list:
    x = rpm_dial_circle_center_x + text_radius * math.cos(math.radians(angle))
    y = rpm_dial_circle_center_y - text_radius * math.sin(math.radians(angle))
    angle = angle-10

    rpm_dial_canvas.create_text(x, y, text=char, font=("Arial", int(round((screen_height * 1)/60, 0))), fill="black")


#----------------------------------------------Open serial connection to Arduino----------------------------------------------
# ser = serial.Serial('/dev/cu.usbserial-110', 9600)

#----------------------------------------------data updation on main window----------------------------------------------
def update_data():
    
    raw_data = '000,100,2000,30,400,500,600,700,800,900,1000,110,120,13.57,140,150,160,no mc fault a :no mc fault b:no mc fault c:no mc fault d; no bms fault a : no bms fault b: no bms fault c: no bms fault d'
    # data order - 0. motor temp  1.mc temp  2.erpm  3.throttle  4.pack current  5.pack voltage  6.charge  7.battery max temp
    #              8.battery min temp  9.mfr  10.bps  11.ac current  12.dc current  13.speed  
    #              14.MC input voltage  15.MC input current  16.LV battery voltage
    #              1.mc faults  2.bms faults
    # raw_data  = ser.readline().decode()
    
    #convert raw data into usable form
    data = raw_data.split(",")
    
    #converting faults to a more organised form
    fault_list = data[-1].split(";")
    bms_faults_string_list = fault_list[-1].split(";")
    bms_faults_list = bms_faults_string_list[0].split(":")
    
    mc_faults_string_list = fault_list[0].split(";")
    mc_faults_list = mc_faults_string_list[0].split(":")
    
    combined_faults_list = bms_faults_list + mc_faults_list
    combined_faults_string_arranged = '\n'.join(combined_faults_list)
    
    # bms_faults_string_arranged = '\n'.join(bms_faults_list)
    # mc_faults_string_arranged = '\n'.join(mc_faults_list)
    
    # #-------------------------calculate speed using erpm and radius of tyres--------------------------
    # erpm = int(data[2])
    # tyre_radius = 20/1000 
    # tyre_circumference = 2*3.14*tyre_radius
    # current_vehicle_calculated_speed = ((erpm/10)*tyre_circumference*60)
    # current_vehicle_calculated_speed = int(round(current_vehicle_calculated_speed, 0))
    # #became useless when speed was directly calculated in the arduino code 
    
    if len(data) >= 10:
        #----------------------------------------------data loggging----------------------------------------------
        #data_to_be_logged = f"\nmotor_temperature:{data[0]}, motor_controller_temperature:{data[1]}, rpm:{data[2]}, throttle:{data[3]},\npack_current:{data[4]}, pack_voltage:{data[5]}, charge:{data[6]},\nbattery_max_temperature:{data[7]}, label_data_battery_min_temperature:{data[8]},\nmfr:{data[9]}, bps:{data[10]}, ac current:{data[11]}, dc current:{data[12]}, speed:{data[13]},\nmc_faults:{fault_list[0]},\nbms_faults:{fault_list[1]}"
        #logging.info(data_to_be_logged)
        

        #----------------------------------------------display values update----------------------------------------------
        # data order - 0. motor temp  1.mc temp  2.erpm  3.throttle  4.pack current  5.pack voltage  6.charge  7.battery max temp
        #              8.battery min temp  9.mfr  10.bps  11.ac current  12.dc current  13.speed
        label_data_motor_temperature.config(text = data[0])
        label_data_motor_controller_temperature.config(text = data[1])
        label_data_throttle.config(text = data[3])
        label_data_pack_current.config(text = data[4]) 
        label_data_pack_voltage.config(text = data[5]) 
        label_data_charge.config(text = data[6])        
        label_data_battery_max_temperature.config(text = data[7])
        label_data_battery_min_temperature.config(text = data[8])
        label_data_mfr.config(text = data[9])
        label_data_bps.config(text = data[9])
        label_data_AC_current.config(text = data[8])
        label_data_DC_current.config(text = data[7])
        #----------------------------------------------display speed and rpm values update----------------------------------------------
        #becomes useless after speedometer introduction
        # label_data_speed.config(text = current_vehicle_calculated_speed)
        # label_data_rpm.config(text = data[2])
        
        #----------------------------------------------display faults update----------------------------------------------
        # label_data_motor_controller_fault.config(text = mc_faults_string_arranged)
        # label_data_bms_fault.config(text = bms_faults_string_arranged)
        
        label_data_all_faults.config(text = combined_faults_string_arranged)
        #----------------------------------------------gather data to be displayed by graphs----------------------------------------------
        plot_1_data.append(int(float(data[4])))
        plot_2_data.append(int(float(data[4])))
        plot_3_data.append(int(float(data[4])))
    
        #remember to delete first entry of above lists else the list will become very big
        del plot_1_data[0]
        del plot_2_data[0]
        del plot_3_data[0]

        #should i convert these 3 functions into 1?
        def plot_graph_1():  
            #plot_1_data = "1,3,2,5,4"  # Get data from user input
            #plot_1_data = plot_1_data.split(",")  # Split data by comma to get individual values
            #plot_1_data = [float(d.strip()) for d in plot_1_data]  # Convert values to float and remove whitespace otherwise they are treated as strings
            #print(plot_1_data)
            
            
            data = plot_1_data[-5:]
            # Clear previous graph
            graph_1_canvas.delete("plot")
            
            # Get canvas size
            canvas_width = graph_1_canvas.winfo_width()
            canvas_height = graph_1_canvas.winfo_height()
            
            # Calculate x and y scaling factors
            x_scale = canvas_width / len(data)
            y_scale = canvas_height / ((max(data)*5)/4)
            
            # Plot data points
            for i in range(len(data)-1):
                x1 = i * x_scale
                y1 = canvas_height - data[i] * y_scale
                if i == len(data)-1:
                    x2 = (i+2) * x_scale
                else:
                    x2 = (i+1) * x_scale
                y2 = canvas_height - data[i+1] * y_scale
                graph_1_canvas.create_line(x1, y1, x2, y2, tags="plot", fill="orange", width=2)
        def plot_graph_2():
            # plot_2_data = "4,1,2,5,4"  # Get data from user input
            # plot_2_data = plot_2_data.split(",")  # Split data by comma to get individual values
            # plot_2_data = [float(d.strip()) for d in plot_2_data]  # Convert values to float and remove whitespace
            #print(dataa)
            
            data = plot_2_data[-5:]
            # Clear previous graph
            graph_2_canvas.delete("plot")
            
            # Get canvas size
            canvas_width = graph_2_canvas.winfo_width()
            canvas_height = graph_2_canvas.winfo_height()
            
            # Calculate x and y scaling factors
            x_scale = canvas_width / len(data)
            y_scale = canvas_height / ((max(data)*5)/4)
            
            # Plot data points
            for i in range(len(data)-1):
                x1 = i * x_scale
                y1 = canvas_height - data[i] * y_scale
                if i == len(data)-1:
                    x2 = (i+2) * x_scale
                else:
                    x2 = (i+1) * x_scale
                y2 = canvas_height - data[i+1] * y_scale
                graph_2_canvas.create_line(x1, y1, x2, y2, tags="plot", fill="yellow3", width=2)
        def plot_graph_3():
            # plot_3_data = "4,1,2,5,4"  # Get data from user input
            # plot_3_data = plot_3_data.split(",")  # Split data by comma to get individual values
            # plot_3_data = [float(d.strip()) for d in plot_3_data]  # Convert values to float and remove whitespace
            #print(dataa)
            
            data = plot_3_data[-5:]
            # Clear previous graph
            graph_3_canvas.delete("plot")
            
            # Get canvas size
            canvas_width = graph_3_canvas.winfo_width()
            canvas_height = graph_3_canvas.winfo_height()
            
            # Calculate x and y scaling factors
            x_scale = canvas_width / len(data)
            y_scale = canvas_height / ((max(data)*5)/4)
            
            # Plot data points
            for i in range(len(data)-1):
                x1 = i * x_scale
                y1 = canvas_height - data[i] * y_scale
                if i == len(data)-1:
                    x2 = (i+2) * x_scale
                else:
                    x2 = (i+1) * x_scale
                y2 = canvas_height - data[i+1] * y_scale
                graph_3_canvas.create_line(x1, y1, x2, y2, tags="plot", fill="medium sea green", width=2)
        
        def update_speed():
            speedometer_canvas.delete("speedometer_dial_pointer")
            current_speed = int(float(data[4]))
            
            speedometer_canvas.create_arc(0, 0, 2*speedometer_radius, 2*speedometer_radius, fill="red2", start=180-(2*current_speed)-1, extent=2, outline="black",width="1", tags="speedometer_dial_pointer")
        def update_rpm():
            rpm_dial_canvas.delete("rpm_dial_pointer")
            current_erpm =  int(round((int(data[4]))/100, 0))
            
            rpm_dial_canvas.create_arc(0, 0, 2*rpm_dial_radius, 2*rpm_dial_radius, fill="red2", start=180-current_erpm-1, extent=2, outline="black",width="1", tags="rpm_dial_pointer")
        
        def update_throttle_bar():
            throttle_canvas.delete("throttle_black_fill")
            throttle_percentage = int(float(data[4]))
            throttle_canvas.create_rectangle(int(round((screen_width * (((throttle_percentage)*986)+64800))/273600, 0))+1, int(round((screen_height * 2)/200, 0))+1, int(round((screen_width * ((100*986)+64800))/273600, 0))-1, int(round((screen_height * 1)/25, 0))-1,fill="black", outline="",width="1", tags="throttle_black_fill")

        
        def toggle_visibility_fault_text():
            if bg_canvas_pg1.itemcget(faults_header_text, 'state') == 'hidden':
                bg_canvas_pg1.itemconfigure(faults_header_text, state='normal')
            else:
                bg_canvas_pg1.itemconfigure(faults_header_text, state='hidden')
        
        global faults_header_text_disappearence_counter
        faults_header_text_disappearence_counter = faults_header_text_disappearence_counter + 1
        if faults_header_text_disappearence_counter == 5:
            faults_header_text_disappearence_counter = 0
            toggle_visibility_fault_text()

        
        plot_graph_1()
        plot_graph_2()
        plot_graph_3()
        update_speed()
        update_rpm()
        update_throttle_bar()
        
    root.after(1, update_data) 
#update_data()
root.after(1, update_data) 


root.mainloop()