from flask import *
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  return ";)"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_live():
  t = Thread(target=run)
  t.start()
