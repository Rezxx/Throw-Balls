import pygame
import OpenGL
import math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Ball import *


balls = []
display = (800,600)
textures = None
boxScale = (10, 10, 10)
cameraPos = [10, 10, 10]
cameraRotate = [45, 45]

# Generating the texture from images
def initTex():
    global textures
    textures = glGenTextures(8)
    for i in range(8):
        Surface = None
        if i == 7:
            Surface = pygame.image.load('Tex/Box.png')
        else:
            Surface = pygame.image.load('Tex/Tex' + str(i) + '.jpg')
        Data = pygame.image.tostring(Surface, "RGBA", 1)
        glBindTexture(GL_TEXTURE_2D, textures[i])
        glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, Surface.get_width(), Surface.get_height(), 0,
                      GL_RGBA, GL_UNSIGNED_BYTE, Data )
        glGenerateMipmap(GL_TEXTURE_2D)
        
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)

# Creating the Ball after mouse being clicked
def createBall(mouse_pos):
    global balls
    mouse_x = mouse_pos[0]
    mouse_y = display[1]- mouse_pos[1]
#     function for mapping perceptive coordinates to object coordinates
#     depth = glReadPixels(mouse_x, mouse_y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT) 
    mouse_z = 0.98 # default number so the ball's z-co will be close to screen
    co = gluUnProject(mouse_x, mouse_y, mouse_z) #Mapping
    
    # determine if the ball is in the box
    inBox = False
    if (co[0] < boxScale[0] and co[0] > - boxScale[0] and
        co[1] < boxScale[1] and co[1] > - boxScale[1] and
        co[2] < boxScale[2] and co[2] > - boxScale[2]):
        inBox = True
    balls.append(Ball(co[0], co[1], co[2], inBox, textures[random.randrange(len(textures) - 1)]))
    
    
# Function for detecting collisions between balls and walls
def collisionDetect(ball):
    camera_z = glGetDoublev(GL_MODELVIEW_MATRIX)[3][2]
    if ball.z > camera_z: ball.speedZ *= -1; ball.z += ball.speedZ
        
    if ball.inBox:
        if ball.x - ball.radius < -boxScale[0]: ball.speedX *= -1; ball.x += ball.speedX
        if ball.x + ball.radius > boxScale[0]: ball.speedX *= -1; ball.x += ball.speedX
        if ball.y - ball.radius < -boxScale[1]: ball.speedY *= -1; ball.y += ball.speedY
        if ball.y + ball.radius > boxScale[1]: ball.speedY *= -1; ball.y += ball.speedY
        if ball.z - ball.radius < -boxScale[2]: ball.speedZ *= -1; ball.z += ball.speedZ
        if ball.z + ball.radius > boxScale[2]: ball.speedZ *= -1; ball.z += ball.speedZ
        
    elif(ball.x < boxScale[0] and ball.x > - boxScale[0] and
        ball.y < boxScale[1] and ball.y > - boxScale[1]):
        if ball.z - ball.radius < boxScale[2]: ball.speedZ *= -1; ball.z += ball.speedZ

# Collision between balls, math stuff
# REF - https://www.pygame.org/project-Sphere+Collisions-620-.html
def collide(ball1, ball2):
    b1Speed = math.sqrt(ball1.speedX**2 + ball1.speedY**2+ ball1.speedZ**2)
    diffX = ball2.x - ball1.x 
    diffY = ball2.y - ball1.y 
    diffZ = ball2.z - ball1.z
    elevationAngle = math.atan(diffY/(math.sqrt(diffX**2+diffZ**2)))
    
    if diffX != 0 and diffZ != 0:
        if diffX > 0:
            if diffZ > 0:   
                angle = math.atan(diffZ/diffX)
            elif diffZ < 0: 
                angle = math.atan(diffZ/diffX)
        elif diffX < 0:
            if diffZ > 0:   
                angle =  math.pi + math.atan(diffZ/diffX)
            elif diffZ < 0: 
                angle = -math.pi + math.atan(diffZ/diffX)
                
        speedX = -b1Speed*math.cos(angle)*math.cos(elevationAngle)
        speedY = -b1Speed*math.sin(elevationAngle)
        speedZ = -b1Speed*math.sin(angle)*math.cos(elevationAngle)
    else:
        if diffX == 0 and diffZ == 0:
            angle = 0
        if diffX == 0 and diffZ != 0:
            if diffZ > 0:   angle = - math.pi / 2
            else:           angle =  math.pi / 2
        if diffX != 0 and diffZ == 0:
            if diffX < 0:   angle =  0
            else:           angle =  math.pi
        speedX = b1Speed*math.cos(angle)*math.cos(elevationAngle)
        speedY = b1Speed*math.sin(elevationAngle)
        speedZ = b1Speed*math.sin(angle)*math.cos(elevationAngle)
        
    ball1.speedX = speedX
    ball1.speedY = speedY
    ball1.speedZ = speedZ
    
#drawing boxes from the coords
def drawBox():
    glBegin(GL_LINES)
    glColor3fv((1,1,1))
    glVertex3fv((100, 0, 0))
    glVertex3fv((-100, 0, 0))
    glVertex3fv((0, 100, 0))
    glVertex3fv((0, -100, 0))
    glVertex3fv((0, 0, 100))
    glVertex3fv((0, 0, -100))
    glEnd()
    
    coord = ((0, 0), (1, 0), (1, 1), (0, 1))
    
    vertices= ((1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
    (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1))

    surfaces = ((0,1,2,3), (3,2,7,6), (6,7,5,4),
    (4,5,1,0), (1,5,7,2), (4,0,3,6))
    
    edges = ((0,1), (0,3), (0,4), (2,1), (2,3), (2,7),
    (6,3), (6,4), (6,7), (5,1), (5,4), (5,7))
    
    glPushMatrix()
    glScalef(*boxScale)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[len(textures) - 1]) 
    glBegin(GL_QUADS)
    for surface in surfaces:
        i = 0
        for vertex in surface:
            glTexCoord2f(*coord[i])
            glVertex3fv(vertices[vertex])
            i += 1
    glEnd()
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

    glDisable(GL_TEXTURE_2D)
    glPopMatrix()
    
#drawing all the balls
def drawBalls():              
    for ball in balls:
        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, ball.texture)
        glTranslatef(ball.x, ball.y, ball.z)
        glRotatef(ball.rotateX,0,1,0)
        glRotatef(ball.rotateY,1,0,0)
        glRotatef(ball.rotateZ,0,0,1)
        sphere = gluNewQuadric()
        gluQuadricTexture(sphere, GL_TRUE)
        gluSphere(sphere, ball.radius, 20, 20)
        glDisable(GL_TEXTURE_2D)  
        glPopMatrix()
            

def main():
    global cameraPos
    pygame.init()
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(90, (display[0]/display[1]), 0.1, 100)
    glMatrixMode(GL_MODELVIEW)
    glShadeModel (GL_FLAT)
    glEnable(GL_DEPTH_TEST)
    initTex()
    
    x_move = 0
    y_move = 0
    z_move = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_move += 0.2
                if event.key == pygame.K_RIGHT:
                    x_move += -0.2

                if event.key == pygame.K_UP:
                    y_move += -0.2
                if event.key == pygame.K_DOWN:
                    y_move += 0.2
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    createBall(pygame.mouse.get_pos())
                if event.button == 4:
                    glTranslatef(0,0,1.0)
                    z_move += 1
                if event.button == 5:
                    glTranslatef(0,0,-1.0)
                    z_move += -1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_move = 0

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_move = 0
        
        cameraPos[0] += x_move
        cameraPos[1] += y_move
        cameraPos[2] += z_move
        
        for ball in balls:
            ball.move(boxScale)
            
        for ball in balls:
            collisionDetect(ball)
        
        for ball1 in balls:
            for ball2 in balls:
                if ball1 != ball2:
                    d = math.sqrt(  ((ball1.x-ball2.x)**2) + ((ball1.y-ball2.y)**2) + ((ball1.z-ball2.z)**2))
                    if d <= (ball1.radius + ball2.radius):
                        collide(ball1,ball2)
        
        
        glClearColor(0,0,0,1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glTranslatef(x_move,y_move,0)
    
        drawBox()
        drawBalls() 
        
        pygame.display.flip()
        pygame.time.wait(10)

main()