'''
    Translate Speech to Text
    Demonstration code only!
    DO NOT USE FOR NOT PRODUCTION

    Shane Frost
    April 2021

    Assumptions
    ===================
    Script will not be running in real-time
    

    Requirements
    ===================
    pip install --upgrade google-cloud-texttospeech
    
'''

import os
import re
import speech_recognition as sr
import nltk
import mutagen
import math

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from mutagen.wave import WAVE
from VideoLengthLib import getVideoLength

# Video is available numerous formats, would expect 2 max in production. 
def ReplaceVideoExtensions(filename):
    for ext in VideoExtensions:
        filename = filename.replace(ext, '.wav')
    return filename.replace('/','\\')

def AddNumberedExtensionToFilename(filename, i):  
    return filename[:-4] + '_' + str(i) + filename[-4:]

def DeleteAllFilesInDirectory(filepath, extension = ''):
    filelist = [ f for f in os.listdir(filepath) if f.endswith(extension) ]
    for f in filelist:
        os.remove(os.path.join(filepath, f))
    

filename = 'No-one is above the law (p1). Geoffrey Robertson.mkv'
baseDirectory = 'E:/Transcripts/'

audiofile = baseDirectory + 'source/' + filename.replace('.mp4','.wav').replace('.mkv','.wav')
chunkLength = 5 # integer minutes

VideoExtensions = ['.mp4','.mkv']

# Clear out the working directory
DeleteAllFilesInDirectory(baseDirectory + 'Working')

# Get the length of the video file
hours, minutes, seconds = getVideoLength(baseDirectory + 'Source/' + filename)

currentHour = 0
currentMinute = 0

r = sr.Recognizer() # initialize the recognizer

for i in range(math.ceil(((hours * 60) + minutes) / chunkLength)): # The count of N minute sections
    TargetVideo = AddNumberedExtensionToFilename(baseDirectory + 'Working/' + filename, i).replace('/','\\')
    TargetAudio = ReplaceVideoExtensions((baseDirectory + 'Working/' + filename).replace('/','\\')[:-4] + '_' + str(i) + filename[-4:])
    
    # Create a split of the video
    os.system('ffmpeg -ss ' + ('0' + str(currentHour))[-2:] + ':' \
          + ('0' + str(currentMinute))[-2:] + ':00  -t ' \
          + str(chunkLength * 60) + ' -i "' \
          + (baseDirectory + 'Source/' + filename).replace('/','\\') + '" -acodec copy "' \
          + TargetVideo)

    # Convert the video into a WAV file.
    os.system('ffmpeg -i "{}" -acodec pcm_s16le -ar 8000 "{}"'.format(TargetVideo, TargetAudio))

    # Process the Audio file
    with sr.AudioFile(TargetAudio) as source:
        audio_data = r.record(source)
        
        try:
            text = r.recognize_google(audio_data, language = 'en-IN', show_all = False)
            print(text)
            with open(baseDirectory + 'Results\\' + filename[:-4] + '.txt', 'a') as o:
                o.write(text)
                o.close()
        except:
            continue

    currentMinute += chunkLength
    if currentMinute > 55:
        currentMinute = 0
        currentHour += 1
    



    

