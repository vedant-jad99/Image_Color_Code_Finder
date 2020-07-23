#!/usr/bin/env python3.8

import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
from urllib import error as e
import urllib.request as urllib2
import os
from pathlib import Path
import numpy as np 
import clipboard

class Ghost_class:
    def __init__(self, root):
        super().__init__()
        self.img = None
        self.root_path = root
        self.url = ""
        self.filename = ""
    def get_Img(self, img):
        self.img = img
    def convert_to_hex(self, tup):
        code = "#"
        for i in tup:
            string = hex(i)
            string = string[2:]
            if len(string) == 1:
                string = "0" + string
            code += dict_hex[string[0]] + dict_hex[string[1]]
        return code
    def return_cord(self, event):
        color_info.delete(0, len(color_info.get()))
        pixels = self.img.getpixel((event.x, event.y))
        if v.get() == 1:
            color_info.insert(0, str(pixels))
        elif v.get() == 2:
            hex_format = self.convert_to_hex(pixels)
            color_info.insert(0, hex_format)

        arr = [[pixels] * 400] * 400
        arr = np.array(arr, dtype=np.uint8).reshape((400, 400, 3))
        img = Image.fromarray(arr)
        img = ImageTk.PhotoImage(img)
        palette = tk.Label(frame3, image=img)
        palette.image = img
        palette.grid(row=0, column=0)
        

def get_path():
    path = filedialog.askopenfilename(title='open')
    return path
def open_img(obj):
    try:
        path = get_path()
        img = Image.open(path)
        img = img.resize((630, 490))
        obj.get_Img(img)
        img = ImageTk.PhotoImage(img)
        lb = tk.Label(frame1, image=img)
        lb.image = img
        lb.grid(row=0, column=0)
        lb.bind("<Button 1>", obj.return_cord)
    except:
        print("Error opening image file")

def accept_url(obj):
    def clear_text():
        last = len(url_in.get())
        name = len(name_in.get())
        url_in.delete(0, last)
        name_in.delete(0, name)
    def get_url():
        url = url_in.get()
        name = name_in.get()
        string = ""
        try:
            obj.url = url
            urllib2.urlopen(obj.url)
            if ".jpg" in name:
                obj.filename = name
                download_img(obj)
                window.destroy()
            else:
                msg = tk.Label(window, text=".jpg extension missing", width=40, fg="#FF0000", padx=10, pady=10)
                msg.grid(row=3, column=0)
        except e.HTTPError as ehttp:
            string = ehttp
            error_msg = tk.Label(window, text=string, width=40, fg="#FF0000", padx=10, pady=10)
            error_msg.grid(row=3, column=0)
        except ValueError as val:
            string = val
            error_msg = tk.Label(window, text=string, width=40, fg="#FF0000", padx=10, pady=10)
            error_msg.grid(row=3, column=0)
        except e.URLError as eurl:
            string = eurl
            error_msg = tk.Label(window, text=string, width=40, fg="#FF0000", padx=10, pady=10)
            error_msg.grid(row=3, column=0)
        

    window = tk.Toplevel(name="download image")
    text = tk.Label(window, text="Enter url of image: ", pady=10, padx=10)
    url_in = tk.Entry(window, relief=tk.SUNKEN, borderwidth=5, width= 40)
    download = tk.Button(window, text="Download", width=10, relief=tk.RAISED, borderwidth=5, command=get_url)
    clear = tk.Button(window, text="Clear", width=10, relief=tk.RAISED, borderwidth=5, command=clear_text)
    filename = tk.Label(window, text="Enter name of file (.jpg): ", pady=10, padx=10)
    name_in = tk.Entry(window, relief=tk.SUNKEN, borderwidth=5, width= 40)

    text.grid(row=0, column=0)
    url_in.grid(row=0, column=1)
    filename.grid(row=1, column=0)
    name_in.grid(row=1, column=1)
    download.grid(row=2, column=0)
    clear.grid(row=2, column=1)
def download_img(obj):
    filename = os.path.join(obj.root_path, obj.filename)
    try:
        urllib2.urlretrieve(obj.url, filename)
    except e.HTTPError as ehttp:
        print(ehttp)
    try:
        img = Image.open(filename)
        img = img.resize((630, 490))
        obj.get_Img(img)
        img = ImageTk.PhotoImage(img)
        lb = tk.Label(frame1, image=img)
        lb.image = img
        lb.grid(row=0, column=0)
        lb.bind("<Button 1>", obj.return_cord)
    except:
        print("Error opening image file")

def copytoclipboard():
    string = color_info.get()
    if len(string) != 0:
        clipboard.copy(string)

if __name__ == "__main__":
    root_path = os.path.join(os.getcwd(), 'Images_Downloads')
    if os.path.exists(root_path):
        pass
    else:
        os.mkdir(root_path)
    dict_hex = {"0": "0", "1": "1","2": "2","3": "3","4": "4","5": "5","6": "6","7": "7","8": "8","9": "9","a": "A","b": "B","c": "C","d": "D","e": "E","f": "F"}
    
    root = tk.Tk()
    frame1 = tk.Frame(root, padx=20, pady=20)
    frame2 = tk.Frame(root, relief=tk.RAISED, borderwidth=5, padx=20, pady=20)
    frame3 = tk.Frame(root, relief=tk.RAISED, borderwidth=5, padx=20, pady=20)
    v = tk.IntVar()
    v.set(1)
    ghost_obj = Ghost_class(root_path)
    load_image = tk.Button(frame2, text="Load Image from device", width=30, relief=tk.GROOVE, padx=5, pady=15, borderwidth=5, command=lambda: open_img(obj=ghost_obj))
    download_image = tk.Button(frame2, text="Download Image from internet", width=30, relief=tk.GROOVE, padx=5, pady=15, borderwidth=5, command=lambda: accept_url(ghost_obj))
    copy_button = tk.Button(frame2, text="Copy to clipboard", width=15, relief=tk.GROOVE, borderwidth=5, padx=5, command=copytoclipboard)

    radio = tk.Radiobutton(frame2, text="RGB format", variable=v, value=1, pady=30)
    radio1 = tk.Radiobutton(frame2, text="Hexcode format", variable=v, value=2, pady=10)
    color_info = tk.Entry(frame2, width=30)

    frame1.grid(row=0, column=1)
    frame2.grid(row=0, column=0)
    frame3.grid(row=0, column=2)
    load_image.grid(row=0, column=0)
    download_image.grid(row=1, column=0)
    copy_button.grid(row=4, column=1)
    radio.grid(row=2, column=0)
    radio1.grid(row=3, column=0)
    color_info.grid(row=4, column=0)
    root.mainloop()

    
