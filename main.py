import vlc
from time import sleep
import json
import os

import voice_info


class iRadio:
    def __init__(self, config_file: str, station_file: str):
        
        self.init(config_file, station_file)
        
        if self.state == 'on':
            self.play()
    
    def init(self, config_file: str, station_file: str):
        print("iRadio init..");
        
        self.config_file = config_file
        self.station_file = station_file
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        
        self.state = "off"
        self.current_station = 0
        
        with open(self.config_file) as c:
            self.config_dict = json.load(c)
            p = self.config_dict['radio_config']
            self.state = p['state']
            self.current_station = p['current_station']
        
        if self.state == "off":
            print("iRadio state: OFF")
        elif self.state == "on":
            print("iRadio state: ON")
            
        self.stations = None
        
        with open(self.station_file) as s:
            station_dict = json.load(s)
            self.stations = station_dict['stations']
            self.station_count = len(self.stations)
        
        print("Loaded \'" + str(self.station_count) + "\' stations..")
        print("Current station: " + str(self.stations[self.current_station]["name"]))
        print("\nDone!")
        
    def get_station_name(self):
        return self.stations[self.current_station]["name"]
    
    def get_station_pronounced_name(self):
        return self.stations[self.current_station]["pronounced"]
    
    def is_playing(self):
        if self.player.play() == -1:
            return False
        else:
            return True
        
    def play(self):
        Media = self.instance.media_new(self.stations[self.current_station]["url"])
        #self.player.audio_set_volume(self.volume)
        #self.getVoiceInfo(self.getStationName())
        Media.get_mrl()
        self.player.set_media(Media)
        
        if self.player.play() == -1:
            print ("Error playing Stream")
            return False
        
        sleep(2)
        self.player.audio_set_volume(60)
        print("\nPlaying.. "  + self.get_station_name())

        voice_info.say_station(self.get_station_pronounced_name())
        sleep(4)
        self.player.audio_set_volume(100)
        #sleep(2)
        #volume_value = self.player.audio_get_volume()
        #print("volume: " + str(volume_value))
        
        self.state = 'on'
        
        #save config
        p = self.config_dict['radio_config']
        p['state'] = self.state
        self.save_config()
        return True
    
    def stop(self):
        self.player.stop()
        
        print("Stop..")
        self.state = 'off'
        
        #save config
        p = self.config_dict['radio_config']
        p['state'] = self.state
        self.save_config()
        
    def next(self):
        self.stop()
        
        if self.current_station == (self.station_count - 1):
            self.current_station = 0
        else:
            self.current_station += 1
            
        if not self.play():
            sleep(2)
            self.next()
            return
        #self.play()
        
        #save config
        p = self.config_dict['radio_config']
        p['current_station'] = self.current_station
        self.save_config()
        
    def prev(self):
        self.stop()
        
        if self.current_station == 0:
            self.current_station = self.station_count - 1
        else:
            self.current_station -= 1
            
        if not self.play():
            sleep(2)
            self.prev()
            return
        #self.play()
        
        #save config
        p = self.config_dict['radio_config']
        p['current_station'] = self.current_station
        self.save_config()
        
    def save_config(self):
        # save config file
        os.remove(self.config_file)
        with open(self.config_file, 'w') as c:
            json.dump(self.config_dict, c)
            
            

if __name__ == "__main__":
    
    radio = iRadio("config_radio.json", "radio_stations.json")
    #radio.play()
    
    while True:
        sleep(60)
        radio.next()

