import pygame
from tkinter import *
from tkinter import Tk,filedialog
import os

class PemutarMusik(Frame):
    def __init__(self,parent):
        Frame.__init__(self, parent)

        self.penampungFile=[]
        self.penampungNama=[]

        self.a = StringVar()
        self.a.set("Play")

        parent.geometry("500x300")
        self.parent = parent

        self.nama = StringVar()
        self.nama.set("Silahkan Buka file") #menampilkan teks silahkan buka file

        self.tampungLokasi=""

        self.berakhir=True
        self.diStop=False
        self.bukaLage=True

        self.fileSudahDiputar=[]
        self.namaSudahDiputar=[]

        self.putarLagi=True

        self.KolomTeks()
        self.buatTeks()
        self.buatTombolPlay()
        self.buatTombolStop()
        self.tombolNext()
        self.buatOpen()
        self.slider()

    def insialisasiFile(self,file,path):
        self.penampungFile.append(path)
        self.penampungNama.append(file)
        self.refreshKolom()
    def refreshKolom(self):
        isi = ""
        no = 1
        for i in self.penampungNama:
            isi += str(no)+".  "+ i + "\n"
            no +=1
        self.setKolom(isi)
    def getFile(self):
        file=''
        if len(self.penampungNama)>0 :
            file = self.penampungFile.pop(0)
            nama = self.penampungNama.pop(0)

            self.fileSudahDiputar.append(file)
            self.namaSudahDiputar.append(nama)

            self.nama.set("Now playing : "+nama)
        self.refreshKolom()
        return file
    def putarMusik(self):
        self.berakhir=True
        pygame.init()
        pygame.mixer.init()
        if self.diStop:
            self.diStop = False
            pygame.mixer.music.unpause()
            self.a.set("Pause")
        else :
            self.b = pygame.mixer.music.get_busy()
            a = len(self.penampungFile)
            if self.b :
                if self.a.get()=="Play" :
                    self.a.set("Pause")
                    pygame.mixer.music.unpause()
                elif self.a.get()=="Pause" :
                    self.a.set("Play")
                    self.pauseAtauStop=False
                    pygame.mixer.music.pause()
                    self.pauseAtauStop=True
            elif  a!=0 :
                ambilFile = self.getFile()
                pygame.mixer.music.load(ambilFile)
                pygame.mixer.music.play()
                self.putarLagi=True
                self.refreshKolom()
                self.getPosisi()
                self.a.set("Pause")

    def stopMusik(self):
        self.b = pygame.mixer.music.get_busy()
        self.diStop = True
        if self.b :
            pygame.mixer.music.play(1,-1)
            pygame.mixer.music.pause()
            self.a.set("Play")
            self.berakhir=False

    def tombolNext(self):
        next = Button(text="Next", command=self.next)
        next.pack(side=LEFT)

    def next(self):
        self.b = pygame.mixer.music.get_busy()
        if self.b :
            pygame.mixer.music.stop()
            self.putarMusik()

    def buatTeks(self):
        teks = Label(textvariable=self.nama, fg="purple", font="Verdana 10 bold")
        teks.pack()

    def buatTombolStop(self):
        tombol = Button(text="Stop", command=self.stopMusik) #button Stop
        tombol.pack(side=LEFT)

    def buatOpen(self):
        tombol = Button(text="Open", command=self.bukaFile) #button open
        tombol.pack(side=LEFT)

    def buatTombolPlay(self):
        tombol = Button(textvariable=self.a, command=self.putarMusik)
        tombol.pack(side=LEFT)
#membuka file dalam bentuk mp3
    def bukaFile(self):
        tipeFile = [('Mp3 file', '*.mp3'), ('All files', '*')]
        bukaFile = filedialog.Open(self, filetypes=tipeFile)
        tipeFile = [('Mp3 file', '*.mp3'), ('All files', '*')]
        bukaFile = filedialog.askopenfilenames(filetypes=tipeFile)
        if bukaFile!="":
            for i in bukaFile :
                lokasi = i
                nama = os.path.basename(lokasi)
                self.insialisasiFile(nama,lokasi)
    def volume(self, nilai):
        v = float(nilai)
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.set_volume(v)

    def slider(self):
        w1 = Scale(from_=0.00, to=1.0,resolution=0.01, command=self.volume, orient=HORIZONTAL, length=300, label='Volume :',showvalue=0)
        w1.pack()
        w1.set(0.50)

    def KolomTeks(self):
        self.T = Text(height=12, width=30)
        self.scrollBar()
        self.T.configure(state=DISABLED)
    def setKolom(self, nilai):
        self.T.config(state=NORMAL)
        self.T.delete('1.0',END)
        self.T.insert(END,nilai)
        self.T.configure(state=DISABLED)

    def scrollBar(self):
        S = Scrollbar()
        S.pack(side=RIGHT, fill=Y)
        self.T.pack(fill=X)
        S.config(command=self.T.yview)
        self.T.config(yscrollcommand=S.set)
    def getPosisi(self):

        pygame.init()
        pygame.mixer.init()
        posisi=pygame.mixer.music.get_pos()
        if posisi==-1 and self.berakhir and self.putarLagi:
            self.putarMusik()
        self.b = pygame.mixer.music.get_busy()
        if len(self.penampungFile) == 0 and self.b == False and self.diStop == False :
            self.nama.set("Pemutaran selesai")
            self.a.set("Play")
            for i in self.fileSudahDiputar :
                self.penampungFile.append(i)
            for i in self.namaSudahDiputar:
                self.penampungNama.append(i)
            self.namaSudahDiputar=[]
            self.fileSudahDiputar=[]
            self.refreshKolom()
            self.putarLagi=False
        elif (len(self.penampungFile)>0 or self.b) and self.putarLagi :
            self.timer = self.parent.after(1000, self.getPosisi)

root = Tk()
PemutarMusik(root)
mainloop()
pygame.quit()

<1>
