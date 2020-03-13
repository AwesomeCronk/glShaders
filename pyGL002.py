import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PyQt5.QtCore import Qt
from OpenGL.GL import (
                       glLoadIdentity, glTranslatef, glRotatef,
                       glClear, glBegin, glEnd,
                       glColor3fv, glVertex3fv,
                       GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,
                       GL_QUADS, GL_LINES
                      )
from OpenGL.GLU import gluPerspective

class mainWindow(QMainWindow):    #Main class.
    def keyPressEvent(self, event):    #This is the keypress detector.
        try:
            key = event.key()
        except:
            key = -1    
        #print(key)
        if key == 16777216:
            exit()

    vertices = [
                (-1, 1, 0)
                (1, 1, 0),
                (1, -1, 0),
                (-1, -1, 0)
               ]
    wires = [
             (0, 1),
             (1, 2),
             (2, 3),
             (0, 3)
            ]
    faces = [
             (0, 1, 2, 3)
            ]
            
    def __init__(self):
        super(mainWindow, self).__init__()
        self.sizeX = 700    #Variables used for the setting of the size of everything
        self.sizeY = 600
        self.setGeometry(0, 0, self.sizeX + 50, self.sizeY)    #Set the window size
        self.initData(self.dataFieldSize)
        
        self.openGLWidget = QOpenGLWidget(self)    #Create the GLWidget
        self.openGLWidget.setGeometry(0, 0, self.sizeX, self.sizeY)
        self.openGLWidget.initializeGL()
        self.openGLWidget.resizeGL(self.sizeX, self.sizeY)    #Resize GL's knowledge of the window to match the physical size?
        self.openGLWidget.paintGL = self.paintGL    #override the default function with my own?

    def nav(self, hVal = 0, vVal = 0, zVal = 0):
        self.zoomLevel += zVal
        self.rotateDegreeH += hVal
        self.rotateDegreeV += vVal
        self.openGLWidget.update()

    def paintGL(self):
        #This function uses shape objects, such as cube() or mesh(). Shape objects require the following:
        #a list named 'vertices' - This list is a list of points, from which edges and faces are drawn.
        #a list named 'wires'    - This list is a list of tuples which refer to vertices, dictating where to draw wires.
        #a list named 'facets'   - This list is a list of tuples which refer to vertices, ditating where to draw facets.
        #a bool named 'render'   - This bool is used to dictate whether or not to draw the shape.
        #a bool named 'drawWires' - This bool is used to dictate whether wires should be drawn.
        #a bool named 'drawFaces' - This bool is used to dictate whether facets should be drawn.
        
        glLoadIdentity()
        gluPerspective(45, self.sizeX / self.sizeY, 0.1, 110.0)    #set perspective?
        glTranslatef(0, 0, self.zoomLevel)    #I used -10 instead of -2 in the PyGame version.
        glRotatef(self.rotateDegreeV, 1, 0, 0)    #I used 2 instead of 1 in the PyGame version.
        glRotatef(self.rotateDegreeH, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        if len(self.shapes) != 0:
            glBegin(GL_LINES)
            for s in self.shapes:
                glColor3fv(s.color)
                if s.render and s.drawWires:
                    for w in s.wires:
                        for v in w:
                            glVertex3fv(s.vertices[v])
            glEnd()
        
            glBegin(GL_QUADS)
            for s in self.shapes:
                glColor3fv(s.color)
                if s.render and s.drawFaces:
                    for f in s.facets:
                        for v in f:
                            glVertex3fv(s.vertices[v])
            glEnd()

app = QApplication([])
window = mainWindow()
window.show()
sys.exit(app.exec_())