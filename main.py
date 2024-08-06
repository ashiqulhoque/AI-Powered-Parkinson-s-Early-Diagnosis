import threading
import pyaudio
import wave
import os
from tkinter import *
from tkinter import filedialog
from lib.RecognitionLib import *

global filePath
global clf

path = "lib/modelxgbtrainedModel.sav"
clf = loadModel(path)
filePath = "unknow"


# Audio record

class App():
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 44100

    frames = []

    def __init__(self, master):

        self.isrecording = False
        self.button1 = Button(app, text='Record', width=12, command=self.startrecording, relief="flat",bg="#00796B", fg="white", borderwidth=0, highlightthickness=0, padx=0, pady=5)
        self.button2 = Button(app, text='Stop Recording', width=12, command=self.stoprecording, relief="flat",bg="#00796B", fg="white", borderwidth=0, highlightthickness=0, padx=5, pady=5)
        self.button1.place(x=300, y=200)
        self.button2.place(x=400, y=200)

    def startrecording(self):

        textTest = "RECORDING"

        textTest1 = "Parkinson's disease is a degenerative disorder of the nervous system that affects movement,                         "
        textTest2 = "often causing tremors, stiffness, and difficulty with balance and coordination. It is caused                 "
        textTest3 = "by the loss of dopamine-producing cells in the brain, which leads to a decline in motor                     "
        testText4 = "function and other symptoms such as depression, anxiety, and sleep disturbances.                              "


        self.textParkiTest = Label(app, text=textTest, font=('bold', '20'), bg='red')
        self.textParkiTest.place(x=210, y=120)

        self.textParkiTest1 = Label(app, text=textTest1, font=('normal', '11'), bg='#64a9a0')
        self.textParkiTest1.place(x=0, y=300)
        self.textParkiTest2 = Label(app, text=textTest2, font=('normal', '11'), bg='#64a9a0')
        self.textParkiTest2.place(x=0, y=320)
        self.textParkiTest3 = Label(app, text=textTest3, font=('normal', '11'), bg='#64a9a0')
        self.textParkiTest3.place(x=0, y=340)
        self.textParkiTest4 = Label(app, text=testText4, font=('normal', '11'), bg='#64a9a0')
        self.textParkiTest4.place(x=0, y=360)

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.sample_format, channels=self.channels, rate=self.fs,
                                  frames_per_buffer=self.chunk, input=True)
        self.isrecording = True

        print('Recording')
        global t
        t = threading.Thread(target=self.record)
        t.start()

    def stoprecording(self):
        if self.isrecording == False:
            print("Press Recoring button first")
        else:
            self.textParkiTest.destroy()
            self.textParkiTest1.destroy()
            self.textParkiTest2.destroy()
            self.textParkiTest3.destroy()
            self.textParkiTest4.destroy()

            self.isrecording = False
            print('recording complete')
            self.filename = "recordingAudio.wav"
            wf = wave.open(self.filename, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.sample_format))
            wf.setframerate(self.fs)
            wf.writeframes(b''.join(self.frames))
            wf.close()

    def record(self):
        self.frames.clear()
        while self.isrecording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)


def chooseFile():
    global filePath
    filePath = filedialog.askopenfilename(initialdir="/C", title="Select a file", filetypes=[("wav file", "*.wav")])
    print("path :", filePath)


def execAI():
    global part_label1
    global part_label2
    global part_label3
    global filePath
    errmsg = "No Recording"

    if ((filePath == "unknow") or (filePath == "")) and os.path.exists("recordingAudio.wav"):
        filePath = "recordingAudio.wav"

    if (filePath != "unknow") and (filePath != ""):
        if predict(clf, filePath):
            # Test label1
            try:
                part_label1
            except NameError:
                part_label1 = None

            if part_label1 is not None:
                part_label1.destroy()
            # Test label2
            try:
                part_label2
            except NameError:
                part_label2 = None

            if part_label2 is not None:
                part_label2.destroy()
            # Test label3
            try:
                part_label3
            except NameError:
                part_label3 = None

            if part_label3 is not None:
                part_label3.destroy()

            # Display answer
            part_label1 = Label(app, text='You have Parkinsons Disease', font=('bold', 20), bg='#B2DFDB', pady=20)
            part_label1.place(x=117, y=100)
        else:
            # Test label1
            try:
                part_label1
            except NameError:
                part_label1 = None

            if part_label1 is not None:
                part_label1.destroy()
            # Test label2
            try:
                part_label2
            except NameError:
                part_label2 = None

            if part_label2 is not None:
                part_label2.destroy()
            # Test label3
            try:
                part_label3
            except NameError:
                part_label3 = None

            if part_label3 is not None:
                part_label3.destroy()

            # Display answer
            part_label2 = Label(app, text="You don't have Parkinson's Disease", font=('bold', 20), bg='#B2DFDB', pady=20)
            part_label2.place(x=80, y=100)
        filePath = "unknow"
    else:
        # Test label1
        try:
            part_label1
        except NameError:
            part_label1 = None

        if part_label1 is not None:
            part_label1.destroy()
        # Test label2
        try:
            part_label2
        except NameError:
            part_label2 = None

        if part_label2 is not None:
            part_label2.destroy()
        #Test label3
        try:
            part_label3
        except NameError:
            part_label3 = None

        if part_label3 is not None:
            part_label3.destroy()

        # Display answer
        part_label3 = Label(app, text=errmsg, font=('bold', 20), bg='#b2dfdb', pady=20)
        part_label3.place(x=210, y=100)

        print(errmsg)
        return errmsg
    if os.path.exists("recordingAudio.wav"):
        os.remove("recordingAudio.wav")


# Create Window
app = Tk()
app.resizable(False, False)

# background
filename = PhotoImage(file="img/Untitled.png")
background_label = Label(app, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Bouton Choose File
add_btn = Button(app, text='Choose File', width=12, command=chooseFile,  relief="flat",bg="#00796B", fg="white", borderwidth=0, highlightthickness=0, padx=0, pady=5)
add_btn.place(x=200, y=200)

# Bouton Detect
add_btn = Button(app, text='Detect', width=12, command=execAI,  relief="flat",bg="#00796B", fg="white", borderwidth=0, highlightthickness=0, padx=0, pady=5)
add_btn.place(x=100, y=200)

# Label
part_label = Label(app, text='Parkinson Detector', bg='#B2DFDB',  font=('bold', 20), pady=10)
part_label.place(x=30, y=10)

if os.path.exists("recordingAudio.wav"):
    os.remove("recordingAudio.wav")

# App title
app.title('Detect Parkinson')
app.geometry('600x400')
App(app)
app.mainloop()

