import os
import subprocess 
import json 
from Core.config import ArusuConfig

# T.B.A.
# Saving a file
# Modifying a file
# Erasing a file

class file_manager() : 
    def __init__(self) : 
        self.custom_path = "./Data/Custom/"
    
    def load_custom(self, Cog_Name : str, File_Name : str) : 
        file_path = self.custom_path + Cog_Name + "/" + File_Name + ".json"