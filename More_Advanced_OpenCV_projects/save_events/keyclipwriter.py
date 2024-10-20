from collections import deque
from threading import Thread
from queue import Queue
import time
import cv2

class KeyClipWriter:
    def __init__(self, bufSize=65,timeout=1.0):
        self.bufsize=bufSize
        self.timeout=timeout
        self.frames=deque(maxlen=bufSize) #framelerin tutulacağı deque
        self.Q=None #threadler arasında haberleşme için kullanılacak queue
        self.writer=None #video yazıcı
        self.thread=None #thread
        self.recording=False #kayıt durumu
    def update(self,frame):
        self.frames.appendleft(frame) #dequeye frame ekle
        if self.recording: #kayıt durumunda ise
            self.Q.put(frame)  #frameyi queueye ekle
    def start(self,outputPath,fourcc,fps):
        # kayıt yaptığımızı belirtin, 
        # video yazıcısını başlatın, # 
        # ve video dosyasına yazılması gereken 
        # karelerin # kuyruğunu başlatın
        self.recording=True
        self.writer=cv2.VideoWriter(outputPath,fourcc
                ,fps,(self.frames[0].shape[1]
            ,self.frames[0].shape[0]),True)
        self.Q=Queue()
        for i in range(len(self.frames),0,-1): #dequeyi queueye ekle
            self.Q.put(self.frames[i-1])
        self.thread=Thread(target=self.write,args=())
        self.thread.daemon=True
        self.thread.start()    
    def write(self):
        while True:
            if not self.recording: #eger kaydimiz bittiyse
                return
            if not self.Q.empty(): #queue bos degilse
                frame=self.Q.get() #queue den frame al
                self.writer.write(frame) #frameyi videoya yaz
            else:
                time.sleep(self.timeout) #queue bos ise bekle
    def flush(self): #tüm kareleri alıp dosyaya atan metod
        while not self.Q.empty(): #queue bos degilse
            frame=self.Q.get()
            self.writer.write(frame)
    def finish(self):
        self.recording=False #kayıt durumunu kapat
        self.thread.join() #threadi bitir
        self.flush() #tüm kareleri alıp dosyaya yaz
        self.writer.release() #video yazıcısını serbest bırak
        

