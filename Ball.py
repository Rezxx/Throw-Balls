import random
import math

class Ball:
    def __init__(self, x, y, z, inBox, texture):
        self.radius = 1
        self.x = x
        self.y = y
        self.z = z
        self.inBox = inBox
        self.texture = texture
        self.speedX = 0.1 * random.randrange(-3, 10)
        self.speedY = 0.1 * random.randrange(-3, 10)
        self.speedZ = 0.1 * random.randrange(-3, -2)
        
        self.rotateRateX = random.randrange(-3, 3)
        self.rotateRateY = random.randrange(-3, 3)
        self.rotateRateZ = random.randrange(-3, 3)
        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
    
    # Moving under the gravity
    def move(self, boxScale):
        if self.speedY >= 0.01 or self.y > -boxScale[1] + self.radius: self.speedY -= 0.01
        self.speedX *= 0.98 if abs(self.speedX) >= 0.01 else 0
        self.speedY *= 0.98 if abs(self.speedY) >= 0.01 else 0
        self.speedZ *= 0.98 if abs(self.speedZ) >= 0.01 else 0
        
        self.rotateX = ( self.rotateX + self.rotateRateX ) % 360 if abs(self.speedX) >= 0.03 else self.rotateX
        self.rotateY = ( self.rotateY + self.rotateRateY ) % 360 if abs(self.speedY) >= 0.03 else self.rotateY
        self.rotateZ = ( self.rotateZ + self.rotateRateZ ) % 360 if abs(self.speedZ) >= 0.03 else self.rotateZ

        
        self.x += self.speedX
        self.y += self.speedY
        self.z += self.speedZ
        