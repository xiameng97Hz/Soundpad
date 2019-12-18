# voice_recognition.py
#
# Author: Xiameng Chen
# Date: 12/04/2019
# Description: Record voice and return the content

import requests
import json
import subprocess

def read_audio(WAVE_FILENAME):
    # function to read audio(wav) file
    with open(WAVE_FILENAME, 'rb') as f:
        audio = f.read()
    return audio


def run():  
	WAVE_OUTPUT_FILENAME = "file.wav"
	URL = 'https://api.wit.ai/speech'
	ACCESS_TOKEN = 'HTQGPKMERH3BEWTVLSAH7MNI3EU4ZUV4'

	cmd='arecord -D plughw:1,0 -d 3 --rate 44100 --format S16_LE -c1 '+ WAVE_OUTPUT_FILENAME
	subprocess.check_output(cmd, shell=True)

	audio = read_audio('file.wav')

	#HTTP request
	headers = {'authorization': 'Bearer ' + ACCESS_TOKEN,'Content-Type': 'audio/wav'}

	#Send the request as post request and the audio as data
	response = requests.post(url = URL, headers = headers,data = audio)

	#Get the text
	data = response.json()
	string = data['_text']
	print(string)
	return string
