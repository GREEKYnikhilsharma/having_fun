from celery import Celery
from chatterbot import ChatBot
from nltk.chat import zen
chatbot=ChatBot("nikhil")
app=Celery('zenbot',broker='amqp://localhost')
@app.task
def chat(x):
 return zen.zen_chat()
 

