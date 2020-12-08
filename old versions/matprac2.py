import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt
import matplotlib.animation as manimation

N = 20;

#gif
#points
#number of iterations on gif
#line triang
#angles
#linear condition of draw (deepth)
#versions of python and libs
#number in iterations in args


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
  def radius(self):
    VertexesCoords = self.getXYcoords()
    a = VertexesCoords[1] - VertexesCoords[0]
    b = VertexesCoords[2] - VertexesCoords[1]
    c = VertexesCoords[0] - VertexesCoords[2]

    S = np.abs(((np.cross(a, b)) / 2))
    return np.sqrt((a ** 2).sum()) * np.sqrt((b ** 2).sum()) * np.sqrt((c ** 2).sum()) / (4 * S)
  def maxSide(self):
    VertexesCoords = self.getXYcoords()
    a = np.sqrt(((VertexesCoords[1] - VertexesCoords[0]) ** 2).sum())
    b = np.sqrt(((VertexesCoords[2] - VertexesCoords[1]) ** 2).sum())
    c = np.sqrt(((VertexesCoords[0] - VertexesCoords[2]) ** 2).sum())   
    return max(a, b, c)

def rescale(v, eps = 0.999):
  center = (v[0] + v[1] + v[2]) / 3
  return np.array([center + (v[0] - center) * eps, center + (v[1] - center) * eps, center + (v[2] - center) * eps])




fig, ax = plt.subplots()
plt.xlim(-1, 1)
plt.ylim(-0.5, 1.5)

#writer = manimation.ImageMagickWriter(fps=10)
writer = manimation.ImageMagickWriter(fps = 5)
writer.setup(fig, "immmgg.gif" , 400)


T0 = ABCTriangle([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
T = ABCTriangle([[1./2., 1./2., 0], [1./2., 0, 1./2.], [0, 1./2., 1./2.]])

ax.add_patch(plt.Polygon(T.getXYcoords(), color = 'black'))
ax.add_line(mp.lines.Line2D ([T0.getXYcoords()[0][0], T0.getXYcoords()[1][0], T0.getXYcoords()[2][0], T0.getXYcoords()[0][0]], [T0.getXYcoords()[0][1], T0.getXYcoords()[1][1], T0.getXYcoords()[2][1], T0.getXYcoords()[0][1]], color="black"))

prevTriangles = []
prevTriangles.append(T)
#tmp = []
#for k in range(N):
#  tmp.append([])
#
#  for i in range(3 ** k):
#    tmp[k].append(prevTriangles[i].newABCTriangle1())
#    tmp[k].append(prevTriangles[i].newABCTriangle2())
#    tmp[k].append(prevTriangles[i].newABCTriangle3())
#  prevTriangles = tmp[k]

for k in range(N):
  plt.title("k = %i" % (k + 1))
  tmp = []
  for t in prevTriangles:
    if (t.maxSide() > 0.03):
      tmp.append(t.newABCTriangle1())
      tmp.append(t.newABCTriangle2())
      tmp.append(t.newABCTriangle3())
  prevTriangles = tmp
  for t in tmp:
    ax.add_patch(plt.Polygon(rescale(t.getXYcoords(), 0.96), color = 'black'))
    ax.add_line(mp.lines.Line2D ([t.getXYcoords()[0][0], t.getXYcoords()[1][0], t.getXYcoords()[2][0], t.getXYcoords()[0][0]], [t.getXYcoords()[0][1], t.getXYcoords()[1][1], t.getXYcoords()[2][1], t.getXYcoords()[0][1]], color="white", linewidth = 0.4))
  
  ax.add_line(mp.lines.Line2D ([rescale(T0.getXYcoords(), 1.01)[0][0], rescale(T0.getXYcoords(), 1.01)[1][0], rescale(T0.getXYcoords(), 1.01)[2][0], rescale(T0.getXYcoords(), 1.01)[0][0]], [rescale(T0.getXYcoords(), 1.01)[0][1], rescale(T0.getXYcoords(), 1.01)[1][1], rescale(T0.getXYcoords(), 1.01)[2][1], rescale(T0.getXYcoords(), 1.01)[0][1]], color="black", linewidth = 1))
  T = ABCTriangle([[1./2., 1./2., 0], [1./2., 0, 1./2.], [0, 1./2., 1./2.]])
  ax.add_patch(plt.Polygon(T.getXYcoords(), color = 'black'))
  writer.grab_frame()




#for t in tmp:
#  for tt in t:
#   if (tt.maxSide() > 0.05):
#    ax.add_patch(plt.Polygon(rescale(tt.getXYcoords(), 1), color = 'black'))
    #ax.add_line(mp.lines.Line2D ([tt.getXYcoords()[0][0], tt.getXYcoords()[1][0], tt.getXYcoords()[2][0], tt.getXYcoords()[0][0]], [tt.getXYcoords()[0][1], tt.getXYcoords()[1][1], tt.getXYcoords()[2][1], tt.getXYcoords()[0][1]], color="white"))



fig.savefig('image.svg' )
plt.show()
