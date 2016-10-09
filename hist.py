#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt

n=5

fig, ax = plt.subplots()

index = np.arange(n)
bar_width = 0.5

opacity = 0.5
#error_config = {'ecolor': '0.3'}

rects1 = plt.bar(index, (42455, 9535, 4373, 997, 6850), bar_width,
                 alpha=opacity,
                 color='b',
                 label='Computation')

plt.xticks(index + bar_width/2, ('[0, 0.02)','[0.2, 0.06)','[0.06, 0.1)','[0.1, 0.5)','[0.5, 1)'))

plt.title("Norm degree with DBSCAN")
plt.xlabel("Norm degree")
plt.ylabel("Number of nodes")

plt.tight_layout()
plt.savefig("plot_db_4.png")

fig, ax = plt.subplots()

rects1 = plt.bar(index, (11171, 38047, 8000, 971, 6021), bar_width,
                 alpha=opacity,
                 color='b',
                 label='Computation')

plt.xticks(index + bar_width/2, ('[0, 0.3)','[0.3, 0.4)','[0.4, 0.6)','[0.6, 0.8)','[0.8, 1]'))

plt.title("(Normalized) closeness with DBSCAN")
plt.xlabel("Closeness")
plt.ylabel("Number of nodes")

plt.tight_layout()
plt.savefig("plot_db_5.png")

fig, ax = plt.subplots()

rects1 = plt.bar(index, (59402, 125, 44, 1283, 3356), bar_width,
                 alpha=opacity,
                 color='b',
                 label='Computation')

plt.xticks(index + bar_width/2, ('0','(0, 1000)','[1000, 10000)','[10000, 100000)','> 100000'))

plt.title("Betweenness with DBSCAN")
plt.xlabel("Betweenness")
plt.ylabel("Number of nodes")

plt.tight_layout()
plt.savefig("plot_db_6.png")

fig, ax = plt.subplots()
rects1 = plt.bar(index, (49956, 2425, 399, 188, 11242), bar_width,
                 alpha=opacity,
                 color='b',
                 label='Computation')

plt.xticks(index + bar_width/2, ('[0, 0.01)','[0.01, 0.02)','[0.02, 0.1)','[0.1, 0.5)','[0.5, 1]'))

plt.title("Eigenvector centrality with DBSCAN")
plt.xlabel("Eigenvector centrality")
plt.ylabel("Number of nodes")

plt.tight_layout()
plt.savefig("plot_db_7.png")

fig, ax = plt.subplots()
rects1 = plt.bar(index, (57342, 896, 3088, 1967, 917), bar_width,
                 alpha=opacity,
                 color='b',
                 label='Computation')

plt.xticks(index + bar_width/2, ('[0, 0.005)','[0.005, 0.01)','[0.01, 0.03)','[0.03, 0.05)','[0.05, 0.11]'))

plt.title("Pagerank with DBSCAN")
plt.xlabel("Pagerank")
plt.ylabel("Number of nodes")

plt.tight_layout()
plt.savefig("plot_db_8.png")

fig, ax = plt.subplots()
rects1 = plt.bar(index, (772, 76103, 6204, 11858, 54194), bar_width,
                 alpha=opacity,
                 color='b',
                 label='Computation')

plt.xticks(index + bar_width/2, ('[0, 0.5)','[0.5, 0.6)','[0.6, 0.8)','[0.8, 0.95)','[0.95, 1)'))

plt.title("Norm degree with community detection")
plt.xlabel("Norm degree")
plt.ylabel("Number of nodes")

plt.tight_layout()
plt.savefig("plot_net_4.png")

fig, ax = plt.subplots()
rects1 = plt.bar(index, (8615, 5058, 8186, 32141, 101131), bar_width,
                 alpha=opacity,
                 color='b',
                 label='Computation')

plt.xticks(index + bar_width/2, ('[0, 0.9)','[0.9, 0.94)','[0.94, 0.97)','[0.97, 0.99)','[0.99, 1]'))

plt.title("(Normalized) closeness with community detection")
plt.xlabel("Closeness")
plt.ylabel("Number of nodes")

plt.tight_layout()
plt.savefig("plot_net_5.png")

fig, ax = plt.subplots()
rects1 = plt.bar(index, (151266, 2853, 418, 268, 326), bar_width,
                 alpha=opacity,
                 color='b',
                 label='Computation')

plt.xticks(index + bar_width/2, ('0','(0, 100)','[100, 500)','[500, 1000)','> 1000'))

plt.title("Betweenness with community detection")
plt.xlabel("Betweenness")
plt.ylabel("Number of nodes")

plt.tight_layout()
plt.savefig("plot_net_6.png")

fig, ax = plt.subplots()
rects1 = plt.bar(index, (7042, 231, 92, 51220, 96546), bar_width,
                 alpha=opacity,
                 color='b',
                 label='Computation')

plt.xticks(index + bar_width/2, ('[0, 0.9)','[0.9, 0.99)','[0.99, 0.995)','[0.995, 1)','1'))

plt.title("Eigenvector centrality with community detection")
plt.xlabel("Eigenvector centrality")
plt.ylabel("Number of nodes")

plt.tight_layout()
plt.savefig("plot_net_7.png")

fig, ax = plt.subplots()
rects1 = plt.bar(index, (65431, 3257, 5037, 3603, 77803), bar_width,
                 alpha=opacity,
                 color='b',
                 label='Computation')

plt.xticks(index + bar_width/2, ('[0, 0.1)','[0.1, 0.1)','[0.1, 0.3)','[0.3, 0.4)','[0.4, 0.5]'))

plt.title("Pagerank with community detection")
plt.xlabel("Pagerank")
plt.ylabel("Number of nodes")

plt.tight_layout()
plt.savefig("plot_net_8.png")
