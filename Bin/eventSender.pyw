from Tkinter import *
from tkFileDialog import *

class eventSender:
    def __init__(self, parent):
        self.top=Toplevel(parent)
        self.createWidgets()
    def createWidgets(self):
        Label(self.top, text='Data Collector:').grid(row=0, stick=W)
        self.serverEntry=Entry(self.top, text='192.168.20.118' )
        self.serverEntry.grid(row=0, column=1)
        Label(self.top, text='Select:').grid(row=1, stick=W)
        self.v=IntVar()
        self.event=Radiobutton(self.top, text='Event Parsing', variable=self.v, value=1)
        self.event.pack(anchor=W)
        self.incident=Radiobutton(self.top, text='Event Parsing', variable=self.v, value=2)
        self.incident.pack(anchor=W)
        
        self.fileButton=Button(self.top, text='Open a File', command=self.openFile)
        self.fileButton.grid(row=3)
        self.actionButton=Button(self.top, text='Run', command=self.run)
        self.actionButton.grid(row=4)
        self.quitButton=Button(self.top, text='Quit')
        self.quitButton.grid(row=4, column=1)
    def openFile(self):
        self.file=askopenfilename()
    def run(self):
        pass

root=Tk()   
app=eventSender(root)
root.wait_window(app.top)
        