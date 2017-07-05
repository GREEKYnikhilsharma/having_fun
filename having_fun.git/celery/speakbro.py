from celery import Celery
import pyttsx
import pyautogui

a1=Celery(__name__)

@a1.task
def speak(say):
 engine=pyttsx.init()
 rate = engine.getProperty('rate')
 engine.setProperty('rate',rate-50)
 engine.setProperty('voice','english')
 engine.say(say)
 engine.runAndWait()
 if(say=='exit'):
  pyautogui.keyDown('altleft')
  pyautogui.hotkey('tab','right','down','right')
  pyautogui.keyUp('altleft')
  pyautogui.hotkey('ctrlleft','c')
