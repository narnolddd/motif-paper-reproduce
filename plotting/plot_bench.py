import matplotlib.pyplot as plt
import numpy as np

# Raphtory side
results = np.zeros((10,10))

for ex in range(10):
    fname = "hpc_output/raphtory-output"+str(ex+1)+".dat"
    with open(fname,'r') as f:
        data = f.readlines()
        res = [(int(line.split(',')[0]), int(line.split(',')[1].strip())/1000) for line in data]
    results[ex,:] = np.array([x[1] for x in res])
    xrange = [x[0] for x in res]

means = results.mean(axis=0)
std = results.std(axis=0)

# Snap side
snap_data = np.zeros((240,10))
for i in range(240):
    fname = "hpc_output/timed_delta_"+str((i+1)*3600)+".txt"
    with open(fname, 'r') as f:
        snap_data[i,:] = np.array([int(l.strip()) for l in f.readlines()[-10:]])

snap_cum = np.cumsum(snap_data, axis=0)
# print(snap_cum)

snap_arr = np.zeros((10,10))
for i in range(9):
    snap_arr[i,:] = snap_cum[24*(i+1)]

print(snap_cum[:25])

snap_all = np.concatenate((snap_cum[:23], snap_arr), axis=0)

snap_means = snap_all.mean(axis=1)
snap_stds = snap_all.std(axis=1)
fig, ax = plt.subplots()

ax.plot(xrange, means, marker = "o", label = "Raphtory")
ax.fill_between(xrange, means - 1.96*std, means + 1.96*std, alpha = 0.3)

ax.plot(list(range(23)) + xrange, snap_means, marker = "x", label = "Snap")
ax.fill_between(list(range(23))+xrange, snap_means - 1.96*snap_stds, snap_means + 1.96*snap_stds, alpha=0.3)
ax.legend()
ax.set_xlabel("Number of windows processed")
ax.set_ylabel("Time (s)")
plt.show()
# plt.savefig("images/snap_raph_bench.png")