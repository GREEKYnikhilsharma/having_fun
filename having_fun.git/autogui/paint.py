import sys
import pyautogui
dis=int(sys.argv[1])
while dis>0:
 pyautogui.dragRel(dis,0,duration=0.2)
 dis=dis-5
 pyautogui.dragRel(0,dis,duration=0.2)
 pyautogui.dragRel(-dis,0,duration=0.2)
 dis=dis-5
 pyautogui.dragRel(0,-dis,duration=0.2)
 pyautogui.click()
