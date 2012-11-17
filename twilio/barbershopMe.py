from datetime import datetime 
with open("/home/nick/music-hack-day.log", "w") as f:
  f.write(str(datetime.now()) + "\n")
