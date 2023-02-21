# Wav格式有很多种，但是wave.open()中支持的是pcm的格式
import os
import wave
import numpy as np

AUDIO_PATH=r'D:\Auto_Cut_Audio\\audio'
TARGET_PATH=r'D:\Auto_Cut_Audio\\res'
SUFFIX=["wav"]

class AudioCutter():
    def __init__(self, filepath, targetpath) -> None:
        self.filepath=filepath
        self.targetpath=targetpath

    def get_all_documents(self, suffix):
        self.documents=[]
        i=os.walk(self.filepath)
        for j,m,n in i:
            for l in n:
                suf=l.split(".")[-1]
                if suf in suffix:
                    self.documents.append(l)
                
    def read_file(self, name):
        filename=AUDIO_PATH+"\\"+name
        file = wave.open(filename, 'r')
        params = file.getparams()
        nchannels, sampwidth, framerate, wav_length = params[:4]
        str_data = file.readframes(wav_length)
        wavedata = np.frombuffer(str_data, dtype=np.short)
        file.close()
        return wavedata, framerate, nchannels, sampwidth, wav_length

    def save_wav(self, data, framerate, nchannels, sampwidth, name):        
        outwave = wave.open(name, 'wb')  
        data_size = len(data)
        nframes = data_size
        comptype = "NONE"
        compname = "not compressed"
        outwave.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
        outwave.writeframes(b''.join(data))
        outwave.close()


    def _cut_audio(self, name, max_len):
        try:
            wavedata, framerate, nchannels, sampwidth, wav_length=self.read_file(name)
            interval=max_len*framerate
            name=name.split(".")[0]
            for i in range(0, len(wavedata), interval):
                data = wavedata[i:interval+i]
                target_name = TARGET_PATH+"\\"+name+"_"+str(int(i/interval))+".wav"  
                print(target_name)
                self.save_wav(data, framerate, nchannels, sampwidth, target_name)
        except:
            info=str(name)+" processing failure, file is skipped"
            print(info)

    def cut_audio(self, max_len=30):
        for doc in self.documents:
            self._cut_audio(doc,max_len)

    def process(self):
        self.get_all_documents(SUFFIX)
        self.cut_audio()

def main():
    audio_cutter=AudioCutter(AUDIO_PATH, TARGET_PATH)    
    audio_cutter.get_all_documents(SUFFIX)
    audio_cutter.process()

main()



