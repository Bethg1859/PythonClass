#******************************************************************************************************************************

#content       = Cube Class

#version       = 0.1.1

#date          = November 21th 

#dependencies  = abstract method

#author        = Elizabeth Guan <yijie.beth.guan@gmail.com>

#******************************************************************************************************************************

from abc import ABC, abstractmethod

class Object:
    def __init__(self, name):
        self.name = name
        self.translation = [0, 0, 0]
        self.rotation    = [0, 0, 0]
        self.scaling     = [1, 1, 1]
    
    def translate(self, x, y, z):
        self.translation = [x, y, z]
        print(f"{self.name} translated to: ({x}, {y}, {z})")
    
    def rotate(self, x, y, z):
        self.rotation = [x, y, z]
        print(f"{self.name} rotated to: ({x}, {y}, {z})")
    
    def scale(self, x, y, z):
        self.scaling = [x, y, z]
        print(f"{self.name} scaled to: ({x}, {y}, {z})")

    def print_status(self):
        pass

class Cube(Object):
    def __init__(self, name):
        super().__init__(name)
        self.coloring = [0, 0, 0]  
        
    def color(self, R, G, B):
        self.coloring = [R, G, B]
        print(f"{self.name} color set to RGB: ({R}, {G}, {B})")

    def print_status(self):
        print(f"  Cube '{self.name}' Status:")
        print(f"  Translation: {self.translation}")
        print(f"  Rotation: {self.rotation}")
        print(f"  Scale: {self.scaling}")
        print(f"  Color: {self.coloring}")

    def update_transform(self, ttype, value):
        # Dictionary mapping transformation types to their corresponding methods
        transform_methods = {
            "translation": self.translate,
            "rotation":    self.rotate,
            "scaling":     self.scale
        }
        # Call the appropriate method with unpacked values
        transform_methods[ttype](*value)

# Creating three cube objects
cube1 = Cube("Cube1")
cube2 = Cube("Cube2")
cube3 = Cube("Cube3")

cube1.translate(1, 2, 3)
cube1.rotate(45, 90, 180)
cube1.scale(2, 3, 2)
cube1.color(35, 200, 10)
cube1.print_status()

cube2.translate(51, 63, 74)
cube2.rotate(36, 48, 72)
cube2.scale(33, 25, 70)
cube2.color(96, 55, 47)
cube2.print_status()

cube3.translate(0.6, 0.8, 0.4)
cube3.rotate(-2, -34, 289)
cube3.scale(80, 66, 49)
cube3.color(215, 246, 79)
cube3.print_status()