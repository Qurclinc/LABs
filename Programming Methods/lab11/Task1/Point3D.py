import math

class Coordinates:
    
    def __init__(self, letter):
        self.letter = letter
        
    def __get__(self, instance, owner):
        return instance.__dict__.get(self.letter)
    
    def __set__(self, instance, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self.letter} must be a number")
        instance.__dict__[self.letter] = float(value)

class Point3D:
    
    x = Coordinates("x")
    y = Coordinates("y")
    z = Coordinates("z")
    
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
        
    @classmethod
    def from_point(self, other):
        return Point3D(other.x, other.y, other.z)
        
    def get_distance(self, other) -> float:
        return (math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2))
        
    def __add__(self, other):
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self
    
    def __sub__(self, other):
        return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self
    
    def __mul__(self, other):
        return Point3D(self.x * other.x, self.y * other.y, self.z * other.z)
    
    def __imul__(self, other):
        self.x *= other.x
        self.y *= other.y
        self.z *= other.z
        return self
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}; {self.y}; {self.z})"