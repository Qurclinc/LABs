class Logger:
    
    def __init__(self):
        self.data = []
    
    def log(self, line):
        self.data.append(line)
    
    def clear(self):
        self.data.clear()
        
    def get_logs(self):
        return self.data.copy()
        
logger = Logger()