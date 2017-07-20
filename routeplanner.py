'''
Skript for a route planner, that ...
'''
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

# create a random set of points, not normal distributed
np.random.seed(42)
nodes = np.random.gamma(10, 2, size=(20, 2))

# calculate the Delaunay triangles
delaunay = Delaunay(nodes)

''' 
# plot
fig, ax = plt.subplots(1,1)

for simp in delaunay.simplices:
	ax.plot(delaunay.points[simp][:,0], delaunay.points[simp][:,1], '-r')
ax.plot(nodes[:,0], nodes[:,1], 'ob', markersize=7)
'''

# convert the triangle edges into segments.
segments = list()

for simp in delaunay.simplices:
	segments.extend([(simp[0], simp[1]), (simp[0], simp[2]), (simp[1], simp[2])])
###print(len(delaunay.simplices) * 3 == len(segments))

# remove duplicates
edges = list(set(segments))
###print('N of segments:', len(segments))
###print('N of edges:', len(edges))
###print(edges[:3]) #edge between point nr 19 and 3, etc.

# euclidean distance
distance_eu = squareform(pdist(nodes, metric='euclidean'))  # pythagoras
distance_ma = squareform(pdist(nodes, metric='cityblock'))  # rechter winkel (manhatten distance)

# create an empty matrix
cs = np.zeros(distance_eu.shape)

# each segment defines the indices of the edges
for seg in segments:
	cs[seg] = distance_eu[seg]
	cs[seg[::-1]] = distance_eu[seg]

# convert the 0.0 weights into NaNs to remove these edges
cs[cs == 0.0] = np.NaN

# calculate it
weights, pre = dijkstra(cs, return_predecessors=True)

# get the actual path from 11 to 19

start = 14
finish = 10
path = [finish]

while True:
	next_segment = pre[start, path[-1]]
	if next_segment == -9999:
		# no connection: break
		break
	elif next_segment == start:
		# finished: break
		break
	else:
		# new segment, add to path
		path.append(next_segment)
path.append(start)
reversed(path)

print('Path %s:%s: ' % (start, finish), ' - '.join(['%d' % _ for _ in reversed(path)]))

# plot
fig, ax = plt.subplots(1, 1, figsize=(8, 8))

# plot the vertices
ax.plot(nodes[:, 0], nodes[:, 1], linestyle='', marker='o', color='gray')

for i, node in enumerate(nodes):
	ax.text(node[0], node[1] * 1.01, '%d' % i, color='gray')

# plot the edges
for edge in edges:
	ax.plot(nodes[edge,][:, 0], nodes[edge,][:, 1], linestyle='-', color='k')

# plot start and end point
ax.plot(nodes[path[0]][0], nodes[path[0]][1], 'or', markersize=9)
ax.plot(nodes[path[-1]][0], nodes[path[-1]][1], 'og', markersize=9)

# plot the path
for i in range(1, len(path)):
	ax.plot(nodes[(path[i - 1], path[i]),][:, 0], nodes[(path[i - 1], path[i]),][:, 1], '-g', lw=2)
