import wolframalpha
import wikipedia
import wx
from pygame import mixer
from subprocess import call
import time
import pywapi
import speech_recognition as sr
import boto3
import os
import sys
import random
import webbrowser
from nytimesarticle import articleAPI

### Global Scope ###

mixer.init()
polly = boto3.client('polly')
beep = lambda x: os.system("echo -n '\a';sleep 0.2;" *x)

### Functions ###
# Talking :: deletes Zed's output the moment it finishes its sentence.
def zedtalk(saywhat):
	spoken_text = polly.synthesize_speech(Text=saywhat, OutputFormat='mp3', VoiceId='Brian')
	with open('output.mp3', 'wb') as f:
		f.write(spoken_text['AudioStream'].read())
		f.close()
	mixer.init()
	mixer.music.load('output.mp3')
	mixer.music.play()
	while mixer.music.get_busy() == True:
		pass
	mixer.quit()
	os.remove('output.mp3')

def wiki(search):
	#wikipedia
	summary = wikipedia.summary(search, sentences=2)
	print summary
	zedtalk(summary)

def newyorktimes(search): #needs to be recoded, doesn't work
	#newyorktimes
	NYTapi = articleAPI('New York Times API CODE GOES HERE')
	client = nyt.Client(NYTapi)
	res = client.query(search, sentences=4)
	summary = next(res.results).text
	print summary

def wolf(search):
	#wolframalpha
	app_id = "API Code for wolframalpha goes here"
	client = wolframalpha.Client(app_id)
	res = client.query(search)
	answer = next(res.results).text
	print answer
	zedtalk(search+" The answer is "+answer )

#main command line
def command(search):
	if "time" in search and "is" in search and "it" in search :
		if "what" in search or "tell" in search :
			timenow = time.localtime()
			timeh= timenow.tm_hour;timem = timenow.tm_min
			if timeh<13: ampm="A.M"
			else: ampm="P.M"
			if timem>9: extra=" "
			else: extra="oh"
			zedtalk("the time is"+str(timeh)+extra+str(timem)+ampm)

	elif "hello" in search or "good morning" in search or "hi" in search :
		zedtalk("Hello, Today is a fantastic day. What can I help you with?")

	elif "open" in search :
		if "google" in search or "internet" in search or "chrome" in search or "chromium" in search or "browser" in search :
			webbrowser.get('chromium-browser').open_new_tab('http://www.google.com')
		elif "google" in search or "internet" in search and "firefox" in search or "browser" in search :
			webbrowser.get('firefox').open_new_tab('http://www.google.com')
		elif "bing" in search or "internet" in search or "chrome" in search or "chromium" in search or "browser" in search :
			webbrowser.get('chromium-browser').open_new_tab('http://www.bing.com')
		elif "bing" in search or "internet" in search and "firefox" in search or "browser" in search :
			webbrowser.get('firefox').open_new_tab('http://www.bing.com')

	elif "news" in search :
		if "technology" in search or "tech" in search or "science" in search :
			webbrowser.get('chromium-browser').open_new_tab('http://www.phys.org')
		elif "political" in search or "bbc" in search :
			webbrowser.get('chromium-browser').open_new_tab('http://www.bbc.com')
		elif "political" in search and "wn" in search or "world news" in search :
			webbrowser.get('chromium-browser').open_new_tab('http://www.wn.com')

	elif "movie" in search :
		if "latest" in search or "times" in search or "showings" in search :
			webbrowser.get('chromium-browser').open_new_tab('http://www.fandango.com')

	elif "weather" in search :
		if "current" in search or "now" in search or "show" :
			webbrowser.get('chromium-browser').open_new_tab('http://www.wunderground.com')

	elif "who" in search or "what" in search :
		if "is" in search :
			try:
				wolf(search)
			except:
				wiki(search)

			# Note: doesn't work yet
	elif "New york times" in search :
		newyorktimes("latest")
		zedtalk("Here are the latest news updates from New York Times")

#booting up
r = sr.Recognizer()
with sr.Microphone() as source:
	r.adjust_for_ambient_noise(source)
zedtalk("Initializing Zed. Adjusting for background noise.")

#Greeting based upon what time it is
timenow = time.localtime()
timeh = timenow.tm_hour;timem = timenow.tm_min
if timeh < 12:
	greeting = ("Good morning Sir, How may I be of assistance?")
elif 12 <= timeh <= 18:
	greeting = ("Good afternoon Sir, How may I be of assistance?")
elif timeh > 18:
	greeting = ("Good evening Sir, How may I be of assistance?")
zedtalk(greeting)


#Frame - GUI
class MyFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None,
			pos=wx.DefaultPosition, size=wx.Size(520,100),
			style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION |
			wx.CLOSE_BOX | wx.CLIP_CHILDREN,
			title="|| Zed ||")
		panel = wx.Panel(self)
		my_sizer = wx.BoxSizer(wx.VERTICAL)
		
		timenow = time.localtime()
		timeh= timenow.tm_hour;timem = timenow.tm_min
		if timeh < 12:
			lbl = wx.StaticText(panel, label="Good morning sir, How may I be of service?")
		elif 12 <= timeh <= 18:
			lbl = wx.StaticText(panel, label="Good afternoon sir, How may I be of service?")
		elif timeh > 18:
			lbl = wx.StaticText(panel, label="Good evening sir, How may I be of service?")
		my_sizer.Add(lbl, 0, wx.ALL, 5)
		self.txt = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER, size=(500,30))
		self.txt.SetFocus()
		self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
		my_sizer.Add(self.txt, 0, wx.ALL, 5)
		panel.SetSizer(my_sizer)
		self.Show()

#Hit enter, then speak to search
	def OnEnter(self, event):
		beep(2)
		input = self.txt.GetValue()
		input = input.lower()
		x=0;y=0;extra=""
		recognized=""
		recengine="google"
		mode=0
		if input == "":
			r = sr.Recognizer()
			with sr.Microphone() as source:
				audio = r.listen(source)
				recognized = r.recognize_google(audio)

			self.txt.SetValue(recognized)
			print recognized
			zedtalk("Searching"+ recognized)			
			
			command(recognized)

			zedtalk("What else can I assist you with?")
		else:
			command(input)

			zedtalk("giggity giggity")

if __name__ == "__main__":
	app = wx.App(True)
	frame = MyFrame()
	app.MainLoop()