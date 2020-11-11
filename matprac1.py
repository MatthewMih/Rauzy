import numpy as np
import matplotlib.pyplot as plt

N = 8;



def ABCtoXY(ABCvertex):
  return [np.sqrt(1./2.) * (ABCvertex[0] - ABCvertex[1]), np.sqrt(3./2.) * ABCvertex[2]]
def newABCvertex1(v):
  return [(v[0] + v[1] + v[2]) / (v[0] + 2. * v[1] + 2. * v[2]), v[1] / (v[0] + 2. * v[1] + 2. * v[2]), v[2] / (v[0] + 2. * v[1] + 2. * v[2])]
def newABCvertex2(v):
  return [v[0] / (2. * v[0] + v[1] + 2. * v[2]), (v[0] + v[1] + v[2]) / (2. * v[0] + v[1] + 2. * v[2]), v[2] / (2. * v[0] + v[1] + 2. * v[2])]
def newABCvertex3(v):
  return [v[0] / (2. * v[0] + 2. * v[1] + v[2]), v[1] / (2. * v[0] + 2. * v[1] + v[2]), (v[0] + v[1] + v[2]) / (2. * v[0] + 2. * v[1] + v[2])]
def newABCTriangle1(T):
  return ABCTriangle(newABCvertex1(T.v1), newABCvertex1(T.v2), newABCvertex1(T.v3))
def newABCTriangle2(T):
  return ABCTriangle(newABCvertex2(T.v1), newABCvertex2(T.v2), newABCvertex2(T.v3))
def newABCTriangle3(T):
  return ABCTriangle(newABCvertex3(T.v1), newABCvertex3(T.v2), newABCvertex3(T.v3))

class ABCTriangle:
  def __init__(self, v1, v2, v3):
    self.v1 = v1
    self.v2 = v2
    self.v3 = v3
  def getXYcoords(self):
    return [ABCtoXY(self.v1),  ABCtoXY(self.v2),  ABCtoXY(self.v3)]

fig, ax = plt.subplots()
plt.xlim(-1, 1)
plt.ylim(-0.5, 1.5)
T0 = ABCTriangle([1, 0, 0], [0, 1, 0], [0, 0, 1])
#ax.add_patch(plt.Polygon(T0.getXYcoords(), True, color = 'black'))
#ax.set_aspect("equal")
T = ABCTriangle([1./2., 1./2., 0], [1./2., 0, 1./2.], [0, 1./2., 1./2.])
ax.add_patch(plt.Polygon(T.getXYcoords(), True, color = 'black'))

prevTriangles = []
prevTriangles.append(T)

for k in range(N):
  tmp = []
  for i in range(3 ** k):
    tmp.append(newABCTriangle1(prevTriangles[i]))
    tmp.append(newABCTriangle2(prevTriangles[i]))
    tmp.append(newABCTriangle3(prevTriangles[i]))
  for t in tmp:
    ax.add_patch(plt.Polygon(t.getXYcoords(), True, color = 'black')) 
  prevTriangles = tmp

#ax.relim()
#ax.autoscale_view()
plt.show()
print(T.getXYcoords())
