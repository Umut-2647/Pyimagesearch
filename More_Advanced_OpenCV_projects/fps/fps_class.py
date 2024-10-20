import datetime

class FPS:
    def __init__(self):
        self.start=None
        self.end=None
        self.numFrames=0
    def start(self): #zamanı başlat
        self.start=datetime.datetime.now()
        return self
    def stop(self): #zamanı durdur
        self.end=datetime.datetime.now()
    def update(self): #frame sayısını arttır
        self.numFrames+=1
    def elapsed(self): #gecen süreyi hesapla
        return (self.end-self.start).total_seconds()
    def fps(self): #fps hesapla
        return self.numFrames/self.elapsed()