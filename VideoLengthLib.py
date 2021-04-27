import subprocess
import re
import math

def getVideoLength(filename):
    process = subprocess.Popen(['E:/Transcripts/ffmpeg/bin/ffmpeg',  '-i', filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = process.communicate()

    result =  re.search("(?<=DURATION        : ).+?(?=\\r\\n)", stdout.decode('utf-8'), flags=0)[0].split(':')
   
    return int(result[0]), int(result[1]), math.ceil(float(result[2].strip('0')))


