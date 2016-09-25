import numpy as np
import matplotlib.pyplot as plt

X=np.array([1,2,4,8,12,24])
Y=np.array([1.10, 0.57, 0.43, 0.35, 0.37,0.45])

plt.plot(X,Y, label = 'Parallel part', marker ='o')
plt.title('Scaling for community detection algorithm with a dataset of size 1000')
plt.xlabel('#cores')
plt.ylabel('Elapsed time')
plt.ylim(ymin = 0, ymax =1.2)
plt.savefig('label_1K.png')
plt.close()

Y1 = np.array([56,28,16,10,8.29,7.61])
plt.plot(X,Y1, label = 'Parallel part', marker ='o')
plt.title('Scaling for community detection algorithm with a dataset of size 10000')
plt.xlabel('#cores')
plt.ylabel('Elapsed time')
plt.ylim(ymin = 0, ymax=57)
plt.savefig('label_10K.png')
plt.close()

Y2 = np.array([226,119,71,42,34,21])
plt.plot(X,Y2, label = 'Parallel part', marker ='o')
plt.title('Scaling for community detection algorithm with a dataset of size 20000')
plt.xlabel('#cores')
plt.ylabel('Elapsed time')
plt.ylim(ymin = 0, ymax=227)
plt.savefig('label_20K.png')
plt.close()

Y3 = np.array([556,289,163,104,69,42])
plt.plot(X,Y3, label = 'Parallel part', marker ='o')
plt.title('Scaling for community detection algorithm with a dataset of size 30000')
plt.xlabel('#cores')
plt.ylabel('Elapsed time')
plt.ylim(ymin = 0, ymax=560)
plt.savefig('label_30K.png')
plt.close()

Y4 = np.array([1080,546,307,184,133,78])
plt.plot(X,Y4, label = 'Parallel part', marker ='o')
plt.title('Scaling for community detection algorithm with a dataset of size 40000')
plt.xlabel('#cores')
plt.ylabel('Elapsed time')
plt.ylim(ymin = 0, ymax=1090)
plt.savefig('label_40K.png')
plt.close()

Z1 = np.array([8235,3680,2104,1206,722,404])
plt.plot(X,Z1, label = 'Parallel part', marker ='o')
plt.title('Scaling for community detection algorithm with a dataset of size 100000')
plt.xlabel('#cores')
plt.ylabel('Elapsed time')
plt.ylim(ymin = 0, ymax=8300)
plt.savefig('label_100K.png')
plt.close()

Z2 = np.array([38309,14808,8847,4739,3173,1684])
plt.plot(X,Z2, label = 'Parallel part', marker ='o')
plt.title('Scaling for community detection algorithm with a dataset of size 200000')
plt.xlabel('#cores')
plt.ylabel('Elapsed time')
plt.ylim(ymin = 0, ymax=38400)
plt.savefig('label_200K.png')
plt.close()

A = np.array([10000,20000,30000,40000,100000])
B = np.array([7.61,21,42,78,404])
plt.plot(A,B,label = 'Parallel part', marker = 'o')
plt.title('Scaling for community detection algorithm with 24 processors (cosilt)')
plt.xlabel('Size of dataset')
plt.ylabel('Elapsed time')
plt.ylim(ymin =0)
plt.xlim(xmin=0)
plt.savefig('24cores.png')
plt.close()

A = np.array([1000,2000,5000,10000])
B = np.array([56,218,1351,5291])
plt.plot(A,B,label = 'Parallel part', marker = 'o')
plt.title('Scaling for comm. det. algorithm with multiprocessing, 24 processors (cosilt)')
plt.xlabel('Size of dataset')
plt.ylabel('Elapsed time')
plt.ylim(ymin =0)
plt.xlim(xmin=0)
plt.savefig('24cores_shared.png')
plt.close()

C = np.array([200000,300000,500000,700000])
D = np.array([1684,4035,10398,20509])
D2 = np.array([2914,6552,18193,36303])
plt.plot(C,D,label = 'Comm. detection', marker = 'o')
plt.plot(C,D2,label = 'DBSCAN', marker = 'v')
plt.title('Scaling with 24 processors (cosilt)')
plt.xlabel('Size of dataset')
plt.ylabel('Elapsed time')
plt.ylim(ymin =0)
plt.xlim(xmin=0)
plt.savefig('24coresb.png')
plt.close()

C = np.array([100000,200000,300000,500000])
D = np.array([534,1828,3570,9769])
D2 = np.array([803,2750,6265,16985])
plt.plot(C,D,label = 'Comm. detection', marker = 'o')
plt.plot(C,D2,label = 'DBSCAN', marker = 'v')
plt.title('Scaling with 64 processors (elcid)')
plt.xlabel('Size of dataset')
plt.ylabel('Elapsed time')
plt.ylim(ymin =0)
plt.xlim(xmin=0)
plt.savefig('64coresb.png')
plt.close()

E = np.array([200000,300000,500000])
F = np.array([25,33,52])
G = np.array([27,33,48])
plt.plot(E,F,label='DBSCAN',marker='o')
plt.plot(E,G,label='Comm. detection', marker='v')
plt.title('Memory consumption on cosilt with 24 proc. (max 64 GB)')
plt.xlabel('Size of dataset')
plt.ylabel('Memory consumption (GB)')
plt.ylim(ymin =0)
plt.savefig('cosilt_mem.png')
plt.close()

E = np.array([200000,300000,500000])
F = np.array([60,77,123])
G = np.array([62,72,122])
plt.plot(E,F,label='DBSCAN',marker='o')
plt.plot(E,G,label='Comm. detection', marker='v')
plt.title('Memory consumption on elcid with 64 proc. (max 128 GB)')
plt.xlabel('Size of dataset')
plt.ylabel('Memory consumption (GB)')
plt.ylim(ymin =0)
plt.savefig('elcid_mem.png')
plt.close()
