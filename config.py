import configparser


class ConfManager():
    def __init__(self, conf_file):        
        self.config = configparser.ConfigParser()
        self.config.read(conf_file)

    def get_conf(self, conf):
        return self.config['DEFAULT'][conf]