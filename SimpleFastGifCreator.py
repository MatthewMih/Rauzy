#version of Python: 2.7.17
#versions of packages:
#matplotlib==2.2.5
#numpy==1.16.6
#https://github.com/MatthewMih/Rauzy

import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt
import matplotlib.animation as manimation

N = 5 #number of iterations
maxSideLength = 0.03 #drawing condition -- length of side < maxSideLength

def ABCtoXY(ABCvertex): #It's function of coordinates transform (a:b:c) -> (x, y)
  u = ABCvertex[0] / (ABCvertex[0] + ABCvertex[1] + ABCvertex[2])
  v = ABCvertex[1] / (ABCvertex[0] + ABCvertex[1] + ABCvertex[2])
  w = ABCvertex[2] / (ABCvertex[0] + ABCvertex[1] + ABCvertex[2])
  return np.array([np.sqrt(1./2.) * (u - v), np.sqrt(3./2.) * w])

#3 types of mappings from Rauzy induction in (a,b,c)-coordinates:
def newABCvertex1(v):
  return np.array([v[0] + v[1] + v[2], v[1], v[2]])
def newABCvertex2(v):
  return np.array([v[0], v[0] + v[1] + v[2], v[2]])
def newABCvertex3(v):
  return np.array([v[0], v[1], v[0] + v[1] + v[2]])

#Class for triangle:
class ABCTriangle: 
  def __init__(self, V):
    self.v = np.array(V)
  
  def getXYcoords(self):
    return np.array([ABCtoXY(self.v[0]),  ABCtoXY(self.v[1]),  ABCtoXY(self.v[2])])
  
  #Functions for creating new triangles using Rauzy induction:
  def newABCTriangle1(self):
    return ABCTriangle([newABCvertex1(self.v[0]), newABCvertex1(self.v[1]), newABCvertex1(self.v[2])])
  def newABCTriangle2(self):
    return ABCTriangle([newABCvertex2(self.v[0]), newABCvertex2(self.v[1]), newABCvertex2(self.v[2])])
  def newABCTriangle3(self):
    return ABCTriangle([newABCvertex3(self.v[0]), newABCvertex3(self.v[1]), newABCvertex3(self.v[2])])
  
  def maxSide(self): #The function of finding the length of the longest side
    VertexesCoords = self.getXYcoords()
    a = np.sqrt(((VertexesCoords[1] - VertexesCoords[0]) ** 2).sum())
    b = np.sqrt(((VertexesCoords[2] - VertexesCoords[1]) ** 2).sum())
    c = np.sqrt(((VertexesCoords[0] - VertexesCoords[2]) ** 2).sum())   
    return max(a, b, c)

def rescale(v, eps = 0.999): #Scaling the triangle, it is necessary for a better quality of the gif-image
  center = (v[0] + v[1] + v[2]) / 3
  return np.array([center + (v[0] - center) * eps, center + (v[1] - center) * eps, center + (v[2] - center) * eps])




fig, ax = plt.subplots() 
plt.xlim(-0.75, 0.75)
plt.ylim(-0.25, 1.25)
writer = manimation.ImageMagickWriter(fps = 0.5)
writer.setup(fig, "SimpleAnimation.gif" , 300)


T0 = ABCTriangle([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) #boundary triangle
T = ABCTriangle([[1./2., 1./2., 0], [1./2., 0, 1./2.], [0, 1./2., 1./2.]]) #central triangle

ax.add_patch(plt.Polygon(T.getXYcoords(), color = 'black')) #central triangle plotting
ax.add_line(mp.lines.Line2D ([T0.getXYcoords()[0][0], T0.getXYcoords()[1][0], T0.getXYcoords()[2][0], T0.getXYcoords()[0][0]], [T0.getXYcoords()[0][1], T0.getXYcoords()[1][1], T0.getXYcoords()[2][1], T0.getXYcoords()[0][1]], color="black", linewidth = 2)) #boundary plotting

plt.title("n = 1")
writer.grab_frame()

prevTriangles = []
prevTriangles.append(T)

for k in range(N - 1): #main cycle
  plt.title("n = %i" % (k + 2))
  tmp = []
  for t in prevTriangles: #cycle to create new triangles layer
    if (t.maxSide() > maxSideLength): #drawing condition check
      tmp.append(t.newABCTriangle1())
      tmp.append(t.newABCTriangle2())
      tmp.append(t.newABCTriangle3())
  prevTriangles = tmp
  for t in tmp: #cycle to plot triangles of current layer
    if (t.maxSide() > maxSideLength): #drawing condition check
      ax.add_patch(plt.Polygon(t.getXYcoords(), color = 'black')) #plotting of triangle body
  writer.grab_frame()
