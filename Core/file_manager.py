# Handles creating / removing custom files

import os
import json 
from Core.error_handler import LogError

class file_manager() : 
    def __init__(self) : 
        #Could not pass any single self arguments to the class as it will be called elsewhere too many times
        pass 
    
    def load_custom(Cog_Name : str, File_Name : str) : 
        try :
            file_path = "./Data/Custom/" + Cog_Name + "/" + File_Name + ".json"
            with open(file_path, 'r', encoding='utf-8') as f :
                file = json.load(f)
            return file 
        except Exception as e :
            LogError(CogName="file_manager", CogFunct="load_custom", Error = e)
    
    def rm_custom(Cog_Name : str, File_Name : str) : 
        file_path = "./Data/Custom/"+ Cog_Name + "/" + File_Name + ".json"
        try : 
            os.remove(file_path)
        except Exception as e:
            LogError(CogName="file_manager", CogFunct="rm_custom", Error = e)
            
    def mk_custom(Cog_Name : str, File_Name : str) : 
        try :
            New_File = {}
            file_path = "./Data/Custom/" + Cog_Name + "/" + File_Name + ".json"
            os.system(f"mkdir ./Data/Custom/{Cog_Name}")
            os.system(f"touch ./Data/Custom/{Cog_Name}/{File_Name}.json")
            with open(f"{file_path}", 'w', encoding='utf-8') as outf :
                    json.dump(New_File, outf, indent=4, separators=(", ", ": "), sort_keys=True, skipkeys=True, ensure_ascii=False)
        except Exception as e:
            LogError(CogName="file_manager", CogFunct="mk_custom", Error = e)
            
    def update_custom(Cog_Name : str, File_Name : str, New_Data : dict) :
        try : 
            file_path = "./Data/Custom/" + Cog_Name + "/" + File_Name + ".json"
            with open(f"{file_path}", 'w', encoding='utf-8') as outf :
                    json.dump(New_Data, outf, indent=4, separators=(", ", ": "), sort_keys=True, skipkeys=True, ensure_ascii=False)
        except Exception as e:
            LogError(CogName="file_manager", CogFunct="update_custom", Error = e)
            
    def list_custom(Cog_Name : str) : 
        try :
            list = ""
            dir_path = "./Data/Custom/" + Cog_Name
            for root,dirs,files in os.walk(dir_path):
                files.sort()
                for filename in files :
                    list += f"{filename} \n"
            return list
        except Exception as e:
            LogError(CogName="file_manager", CogFunct="list_custom", Error = e)