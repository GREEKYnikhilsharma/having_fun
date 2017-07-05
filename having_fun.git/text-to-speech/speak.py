import sys
import pyttsx
engine = pyttsx.init()
rate = engine.getProperty('rate')
engine.setProperty('rate',rate-50)
engine.setProperty('voice','english')
engine.say(sys.argv[1:])
engine.runAndWait()
#engine.say(sys.argv[1:])
