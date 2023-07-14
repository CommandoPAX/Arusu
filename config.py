# Plugin gérant la config d'Arusu

import json
import platform

class ArusuConfig() : 
    def __init__(self) :
        if platform.system() == "Windows" :
            with open(r".\config.json", 'r', encoding='utf-8') as f:
                self.DATA = json.load(f)
        if platform.system() == "Linux" :
            with open("./config.json", 'r', encoding='utf-8') as f:
                self.DATA = json.load(f)
    
    def update(self, index, value) : 
        try :
            self.DATA[index] = value
            if platform.system == "Linux" :
                with open("./config.json", 'w', encoding='utf-8') as outf :
                    json.dump(self.DATA, outf, indent=4, separators=(", ", ": "), sort_keys=True, skipkeys=True, ensure_ascii=False)
            if platform.system == "Windows" :
                with open(r".\config.json", 'w', encoding='utf-8') as outf :
                    json.dump(self.DATA, outf, indent=4, separators=(", ", ": "), sort_keys=True, skipkeys=True, ensure_ascii=False)
            print(index, "has been updated to", value)
        except Exception as e:
            print("Value could not be updated") 
            print(e)
                
