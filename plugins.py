import importlib
plugins = {}

class PluginManager():
    
    async def importall():
        for cog in plugins.index() :
            importlib.import_module(name = plugins[cog])
            
    async def addcog(cogname) : 
        plugins[cogname] = "./plugins/" + cogname
        
    async def rmcog(cogname) : 
        del plugins[cogname]