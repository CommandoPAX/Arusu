# Plugin gérant la config d'Arusu

import json
from discord.ext import commands, tasks
import os

class ArusuConfig() : 
    def __init__(self) :
        with open(r".\config.json", 'r') as f:
            self.DATA = json.load(f)
    
    def update(self, index, value) : 
        try :
            self.DATA[index] = value
            with open(r".\config.json", 'w') as outf :
                json.dump(self.DATA, outf, indent=4, separators=(", ", ": "), sort_keys=True, skipkeys=True, ensure_ascii=False)
            print(index, "has been updated to", value)
        except Exception as e:
            print("Value could not be updated") 
            print(e)
                
