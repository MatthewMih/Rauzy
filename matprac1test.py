import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt

N = 8;



def ABCtoXY(ABCvertex):
  u = ABCvertex[0] / (ABCvertex[0] + ABCvertex[1] + ABCvertex[2])
  v = ABCvertex[1] / (ABCvertex[0] + ABCvertex[1] + ABCvertex[2])
  w = ABCvertex[2] / (ABCvertex[0] + ABCvertex[1] + ABCvertex[2])
  return np.array([np.sqrt(1./2.) * (u - v), np.sqrt(3./2.) * w])
def newABCvertex1(v):
  return np.array([v[0] + v[1] + v[2], v[1], v[2]])
def newABCvertex2(v):
  return np.array([v[0], v[0] + v[1] + v[2], v[2]])
def newABCvertex3(v):
  return np.array([v[0], v[1], v[0] + v[1] + v[2]])

class ABCTriangle:
  def __init__(self, V):
    self.v = np.array(V)
  def getXYcoords(self):
    return np.array([ABCtoXY(self.v[0]),  ABCtoXY(self.v[1]),  ABCtoXY(self.v[2])])
  def newABCTriangle1(self):
    return ABCTriangle([newABCvertex1(self.v[0]), newABCvertex1(self.v[1]), newABCvertex1(self.v[2])])
  def newABCTriangle2(self):
    return ABCTriangle([newABCvertex2(self.v[0]), newABCvertex2(self.v[1]), newABCvertex2(self.v[2])])
  def newABCTriangle3(self):
    return ABCTriangle([newABCvertex3(self.v[0]), newABCvertex3(self.v[1]), newABCvertex3(self.v[2])])

def rescale(v, eps = 0.999):
  center = (v[0] + v[1] + v[2]) / 3
  return np.array([center + (v[0] - center) * eps, center + (v[1] - center) * eps, center + (v[2] - center) * eps])
fig, ax = plt.subplots()
plt.xlim(-1, 1)
plt.ylim(-0.5, 1.5)
T0 = ABCTriangle([[1, 0, 0], [0, 1, 0], [0, 0, 1]])


T = ABCTriangle([[1./2., 1./2., 0], [1./2., 0, 1./2.], [0, 1./2., 1./2.]])
ax.add_patch(plt.Polygon(T.getXYcoords(), True, color = 'black'))




prevTriangles = []
prevTriangles.append(T)
tmp = []
for k in range(N):
  tmp.append([])

  for i in range(3 ** k):
    tmp[k].append(prevTriangles[i].newABCTriangle1())
    tmp[k].append(prevTriangles[i].newABCTriangle2())
    tmp[k].append(prevTriangles[i].newABCTriangle3())
  prevTriangles = tmp[k]

#i = N - 1
#while i > 0:
#  for j in range(3 ** i):
#    ax.add_patch(plt.Polygon(rescale(tmp[i][j].getXYcoords(), 1), color = 'black'))
#  i -= 1


for t in tmp:
  for tt in t:
    ax.add_patch(plt.Polygon(rescale(tt.getXYcoords(), 1), color = 'black'))
for t in tmp:
  for tt in t:
    ax.add_line(mp.lines.Line2D ([tt.getXYcoords()[0][0], tt.getXYcoords()[1][0], tt.getXYcoords()[2][0], tt.getXYcoords()[0][0]], [tt.getXYcoords()[0][1], tt.getXYcoords()[1][1], tt.getXYcoords()[2][1], tt.getXYcoords()[0][1]], color="white"))

plt.show()
