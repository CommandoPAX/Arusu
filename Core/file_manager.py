import os
import subprocess 
import json 
from Core.config import ArusuConfig
from Core.error_handler import LogError

# T.B.A.
# Saving a file
# Modifying a file
# Erasing a file

class file_manager() : 
    def __init__(self) : 
        self.custom_path = "./Data/Custom/"
        self.CogName = "file_manager"
        self.file = {}
    
    def load_custom(self, Cog_Name : str, File_Name : str) : 
        file_path = self.custom_path + Cog_Name + "/" + File_Name + ".json"
        with open(file_path, 'r', encoding='utf-8') as f :
                    self.file = json.load(f)
        return self.file 
    
    def rm_custom(self, Cog_Name : str, File_Name : str) : 
        file_path = self.custom_path + Cog_Name + "/" + File_Name + ".json"
        try : 
            os.remove(file_path)
        except Exception as e:
            LogError(CogName=self.CogName, CogFunct="rm_custom", Error = e)
            
    def mk_custom(self, Cog_Name : str, File_Name : str) : 
        try :
            New_File = {}
            file_path = self.custom_path + Cog_Name + "/" + File_Name + ".json"
            try :
                subprocess.run([f"touch {file_path}"], check = True)
            except Exception as e:
                subprocess.run([f"cd {self.custom_path}",f"mkdir {Cog_Name}", f"cd {Cog_Name}", f"touch {File_Name}.json", "cd ../../.."], check = True)
            with open(f"{file_path}", 'w', encoding='utf-8') as outf :
                    json.dump(New_File, outf, indent=4, separators=(", ", ": "), sort_keys=True, skipkeys=True, ensure_ascii=False)
        except Exception as e:
            LogError(CogName=self.CogName, CogFunct="mk_custom", Error = e)
            
    def list_custom(self, Cog_Name : str, File_Name : str) : 
        try :
            list = ""
            dir_path = self.custom_path + Cog_Name
            for root,dirs,files in os.walk(dir_path):
                files.sort()
                for filename in files :
                    list += f"{filename} \n"
            return list
        except Exception as e:
            LogError(CogName=self.CogName, CogFunct="list_custom", Error = e)
            
    def test(self) : 
        try :
            return subprocess.run(["ls"], check = True)
        except Exception as e:
            LogError(CogName=self.CogName, CogFunct="test", Error = e)