
'''
Team class 
'''

class Team:
    def __init__(self, name, weight):
        self._name = name
        self._weight = weight

    
    def name(self):
        return self._name
    
    
    def weight(self):
        return self._weight
    
    
    
    def __str__(self):
        return f"{self._name} ({round(self._weight, 2)})"
    
        
