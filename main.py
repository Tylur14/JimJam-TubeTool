import pytube
from pytube import YouTube
import PIL
from PIL import ImageTk, Image
from tkinter import Tk, Label
import urllib
import os
import tkinter as tk

# refs:
# resizing image - https://stackoverflow.com/questions/4066202/resizing-pictures-in-pil-in-tkinter/32803004
# panel.pack_propagate(0) - https://stackoverflow.com/questions/44826267/setting-tk-frame-width-and-height?rq=1
# setting button function - https://www.delftstack.com/howto/python-tkinter/how-to-pass-arguments-to-tkinter-button-command/
# adding image - https://stackoverflow.com/questions/23901168/how-do-i-insert-a-jpeg-image-into-a-python-tkinter-window
# prevent window resize - https://stackoverflow.com/questions/37446710/how-to-make-a-tkinter-window-not-resizable


# todo:
# support user link input
# support UI
    # display thumbnail preview and other video data to user
# support user save location input
# support user renaming but if blank rename it

# where to save to, defaults
SAVE_PATH = "C:/Users/Jim/Videos/YouTube Downloads"

# YouTube video URL, defaults
link = "https://www.youtube.com/watch?v=K_vxWGHaYV8"


# function check_link
# returns bool
# uses YouTube to check if valid link
# if false disables download buttons
def check_link():
    try: 
        #object creation using YouTube which was imported in the beginning 
        yt = pytube.YouTube(linkInput.get()) 
        downloadVideo.configure(state="normal")
        downloadAudio.configure(state="normal")
        set_preview()
    except: 
        i = ImageTk.PhotoImage(Image.open("placeholder.png").resize((640,360),Image.ANTIALIAS))
        panel.configure(image = i)
        panel.image = i
        downloadVideo.configure(state="disabled")
        downloadAudio.configure(state="disabled")
        statusLabel.configure(text="Cannot find the video...") #to handle exception
    

# function set_preview
# takes in YouTube obj
# gets and displays label image for video thumbnail
# gets and sets text label for video name
# enables download buttons
def set_preview():
    yt = pytube.YouTube(linkInput.get())
    image=urllib.request.URLopener()
    image.retrieve(yt.thumbnail_url,"thumbnail.png")
    i = ImageTk.PhotoImage(Image.open("thumbnail.png").resize((640,360),Image.ANTIALIAS))
    panel.configure(image = i)
    panel.image = i
    statusLabel.configure(text="Video is ready to download!")

# function get_video
# retrieves valid YouTube video to data stream
def get_video(url = link):
    try: 
        #object creation using YouTube which was imported in the beginning 
        yt = pytube.YouTube(linkInput.get()) 
    except: 
        print("Connection error or invalid video!") #to handle exception 
  
    #filters out all the files with "mp4" extension 
    mp4files = yt.streams.get_highest_resolution()
  
    #get the video with the extension and resolution passed in the get() function 
    d_video = mp4files 
    try: 
        #downloading the video
        d_video.download(SAVE_PATH,nameInput.get()) 
    except: 
        print("Error: unable to complete video download")

def get_audio(url = link):
    try: 
        #object creation using YouTube which was imported in the beginning 
        yt = pytube.YouTube(linkInput.get()) 
    except: 
        print("Connection error or invalid video!") #to handle exception 
  
    #get the video with the extension and resolution passed in the get() function
    audio = yt.streams.get_audio_only() 
    try: 
        #downloading the video
        audio.download(SAVE_PATH,nameInput.get())
    except: 
        print("Error: unable to complete video download")

window = tk.Tk()
window.title('TubeTool')
window.resizable(False,False)
window.geometry("700x470")
headerFrame = tk.Frame(window)
headerFrame.pack()

bodyFrame = tk.Frame(window)
bodyFrame.pack()

footerFrame = tk.Frame(window)
footerFrame.pack(side=tk.BOTTOM)

sv = tk.StringVar()
sv.trace("w", lambda name, index, mode, sv=sv: check_link())
linkInput = tk.Entry(headerFrame,
    width=60,
    textvariable=sv
    )


img = ImageTk.PhotoImage(Image.open("placeholder.png").resize((640,360),Image.ANTIALIAS))
panel = tk.Label(bodyFrame, image = img)

nameInput = tk.Entry(footerFrame,
    width=60
    )

downloadVideo = tk.Button(footerFrame,
    state="disabled",
    text="Download Video",
    width=20,
    height=2,
    command=lambda: get_video(linkInput.get()) 
    )

downloadAudio = tk.Button(footerFrame,
    state="disabled",
    text="Download Audio",
    width=20,
    height=2,
    command=lambda: get_audio(linkInput.get()) 
    )

statusLabel = tk.Label(headerFrame,
    width=60,
    text="Enter a video link"
    )


linkInput.pack(side=tk.TOP)
statusLabel.pack()
panel.pack()
nameInput.pack()
downloadVideo.pack(side=tk.RIGHT)
downloadAudio.pack(side=tk.LEFT)


window.mainloop()