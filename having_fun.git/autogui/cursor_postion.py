import pyautogui
import threading
def test():
 pyautogui.position()
 
try:
 while True:
  threading.Timer(0.25,test).start()
  
except KeyboardInterrupt:
 print("\nSuccess\n")
