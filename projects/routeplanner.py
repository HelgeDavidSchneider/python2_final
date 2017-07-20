'''
Skript for a route planner, that ...
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from scipy.spatial.distance import pdist, squareform
from scipy.sparse.csgraph import \
	dijkstra  # , floyd_warshall, bellman_ford, johnson


def nodes_plot():
	np.random.seed(42)
	nodes = np.random.gamma(10, 2, size=(20, 2))

	fig, ax = plt.subplots(1, 1, figsize=(8, 8))
	# plot the vertices
	ax.plot(nodes[:, 0], nodes[:, 1], linestyle='', marker='o', color='gray')
	for i, node in enumerate(nodes):
		ax.text(node[0], node[1] * 1.01, '%d' % i, color='gray')

	return plt.show()


def routeplanner(start, finish, distance):
	if start not in range(20) or finish not in range(20) \
			or distance not in ['eucledian', 'manhatten']:
		raise ValueError('Wrong Input. '
						 '\nstart and finish have to be int between 0 and 19. '
						 '\ndistance can only be eucledian or manhatten.')

	np.random.seed(42)
	nodes = np.random.gamma(10, 2, size=(20, 2))
	delaunay = Delaunay(nodes)
	segments = list()

	for simp in delaunay.simplices:
		segments.extend(
			[(simp[0], simp[1]), (simp[0], simp[2]), (simp[1], simp[2])])

	edges = list(set(segments))

	if distance == 'eucledian':
		dis = squareform(pdist(nodes, metric='euclidean'))  # pythagoras
	elif distance == 'manhatten':
		dis = squareform(pdist(nodes, metric='cityblock')) #90°

	## creating the weight matrix

	cs = np.zeros(dis.shape)
	# each segment defines the indices of the edges
	for seg in segments:
		cs[seg] = dis[seg]
		cs[seg[::-1]] = dis[seg]
	cs[cs == 0.0] = np.NaN

	weights, pre = dijkstra(cs, return_predecessors=True)

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

	title = 'Path %s to %s: ' % (start, finish), ' - '.join(
		['%d' % _ for _ in reversed(path)])

	# plot
	fig, ax = plt.subplots(1, 1, figsize=(8, 8))

	# plot the vertices
	ax.plot(nodes[:, 0], nodes[:, 1], linestyle='', marker='o', color='gray')

	for i, node in enumerate(nodes):
		ax.text(node[0], node[1] * 1.01, '%d' % i, color='gray')

	# plot the edges
	for edge in edges:
		ax.plot(nodes[edge,][:, 0], nodes[edge,][:, 1], linestyle='-',
				color='k')

	# plot the path
	for i in range(1, len(path)):
		ax.plot(nodes[(path[i - 1], path[i]),][:, 0],
				nodes[(path[i - 1], path[i]),][:, 1], '-g', lw=2)

	# plot start and end point
	ax.plot(nodes[path[0]][0], nodes[path[0]][1], 'or', markersize=9)
	ax.plot(nodes[path[-1]][0], nodes[path[-1]][1], 'og', markersize=9)

	plt.suptitle(title[0] + title[1])

	return plt.show()
