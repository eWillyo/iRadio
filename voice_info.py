import os
import datetime


VOICE_COMMAND = "(echo \"%s\" | uconv -f utf-8 -t iso-8859-2 | festival --tts --language czech) &"

day_of_week = ["pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle"]
month = ["ledna", "února", "března", "dubna", "května", "června", "července", "srpna", "září", "října", "listopadu", "prosince"]


def say_text(text):
    #print(text)
    os.popen(VOICE_COMMAND % (text))
    return text

def say_station(station):
    command = "Posloucháte %s" % station
    #print(command)
    os.popen(VOICE_COMMAND % (command))
    return command
    
def get_time():
    now = datetime.datetime.now()
    weekday = now.weekday()
    return "Je právě %d %d a je %s %d %s" % (now.hour, now.minute, day_of_week[weekday], now.day, month[now.month-1])

def say_time():
    command = get_time()
    #print(command)
    os.popen(VOICE_COMMAND % (command))
    return command
