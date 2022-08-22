import json

import matplotlib.pyplot as plt
import numpy as np

#plt.rcParams['font.size'] = 18

with open('./cpu-load/cpu-load.json') as fp:
    json_data = json.load(fp)

with open('./base/base.json') as basefp:
    base = json.load(basefp)

thread = json_data['thread'] #rt prio: 99~0
min_time = []
max_time = []
avg_time = []

for key in thread:
    min_time.append(thread[key]['min'])
    max_time.append(thread[key]['max'])
    avg_time.append(thread[key]['avg'])

max_var = np.var(max_time)
max_std = np.std(max_time, ddof=1)
avg_var = np.var(avg_time)
avg_std = np.std(avg_time, ddof=1)
print(max_var)
print(max_std)
print(avg_var)
print(avg_std)

base_thread = base['thread'] #rt prio: 99~0
base_min_time = []
base_max_time = []
base_avg_time = []

for key in base_thread:
    base_min_time.append(base_thread[key]['min'])
    base_max_time.append(base_thread[key]['max'])
    base_avg_time.append(base_thread[key]['avg'])

y1 = []
y2 = []
y3 = []

for x in range(1,50): #41~99
    y1.append(x)
    y2.append(avg_time[49-x])
    y3.append(base_avg_time[49-x])

y1points = np.array(y1)
y2points = np.array(y2)
y3points = np.array(y3)

#plt.xlim(49,0)

X = np.arange(49)
fig = plt.figure()
ax = fig.add_axes([0.1,0.1,0.8,0.8])
ax.bar(X + 51.00, y2points, color = 'r', width = 0.33, label='hybrid load(IO mainly)')
ax.bar(X + 51.33, y3points, color = 'g', width = 0.33, label='base')
plt.xticks([51,60,70,80,90,99])
#plt.yscale("log")

plt.legend()
plt.xlabel("realtime thread priority")
plt.ylabel("latency")
plt.title("average latency of hybrid load(IO mainly)")

#plt.show()
