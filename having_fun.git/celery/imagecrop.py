from PIL import Image,ImageChops
from celery import Celery
app=Celery('imagecrop',broker='pyamqp://')
@app.task
def add(i):
 #bg=Image.new(i.mode,i.size,i.getpixel(0,0))
 #diff=ImageChops.difference(i,bg)
 #diff=ImageChops.add(diff,diff,2.0,-100)
 #if bbox:
 # i=i.crop(bbox)
 # i.show()
 print(i)
