from utils.json_util import read_json


class __ConfigManager(type):
    __instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            instance = super().__call__(*args, **kwargs)
            cls.__instances[cls] = instance
        return cls.__instances[cls]
    
    
class ConfigManager(metaclass=__ConfigManager):
    def read_file(self, config_file_path: str):
        self.__config = read_json(config_file_path)
        
    def get(self):
        return self.__config
    
    