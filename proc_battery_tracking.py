import os
import json
import re

import time
import datetime

def sorted_nicely(data): 
    '''
    Sort the given iterable in the way that humans expect.
    ''' 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key[0])] 
    return sorted(data, key=alphanum_key)


"""

G5

"""

# Open the data
android_data = 'battery_tracking.json'
with open(android_data, 'r') as f:
	data = json.load(f)

# Organize the data
orgdata = {}

d = data[0]['data']
xaxis = data[0]['xaxis']

for c, x in enumerate(xaxis):
	if str(x) not in orgdata:
		orgdata[str(x)] = {
			'log': None, 'battery-before': None, 'battery-after': None
		}

	currname = None
	pname = list(d[c].keys())[0]
	names = ['live_backing', 'battery-before', 'battery-after']
	for name in names:
		if name in pname:
			currname = name

	if currname == 'live_backing':
		orgdata[str(x)]['log'] = d[c][pname][-1]
	elif currname == 'battery-before':
		orgdata[str(x)]['battery-before'] = d[c][pname]
	else:
		orgdata[str(x)]['battery-after'] = d[c][pname]

st_matcher = re.compile(r"\[taskcluster\s+(.*)\]")
start_times = []
charge_levels = []
for trial, trial_info in orgdata.items():
	st = st_matcher.findall(trial_info['log'])[0]
	cl = None
	for line in trial_info['battery-after']:
		if 'level:' not in line:
			continue
		cl = int(line.split('level: ')[-1])
		break
	start_times.append(st)
	charge_levels.append(cl)

print(charge_levels)
print(start_times)

md = sorted_nicely([
	(start_times[c], charge_levels[c])
	for c,_ in enumerate(charge_levels)
])

print(md)

newmd = []
for entry in md:
	stime = entry[0]
	# '2020-02-15T05:32:08.156Z'
	ts = time.mktime(
		datetime.datetime.strptime(
			stime.split('.')[0], "%Y-%m-%dT%H:%M:%S"
		).timetuple()
	)
	newmd.append((ts, entry[1]))

print(newmd)

## PLOT
from matplotlib import pyplot as plt

plt.figure()
mg_len = len(newmd)
mg_lost = 100 - newmd[-1][1]
plt.scatter(
	[((ts-newmd[0][0])/60)/60 for ts, cl in newmd],
	[cl for ts, cl in newmd],
	color='b'
)

"""

P2

"""

# Open the data
android_data = 'battery_tracking_p2.json'
with open(android_data, 'r') as f:
	data = json.load(f)

# Organize the data
orgdata = {}

d = data[0]['data']
xaxis = data[0]['xaxis']

for c, x in enumerate(xaxis):
	if str(x) not in orgdata:
		orgdata[str(x)] = {
			'log': None, 'battery-before': None, 'battery-after': None
		}

	currname = None
	pname = list(d[c].keys())[0]
	names = ['live_backing', 'battery-before', 'battery-after']
	for name in names:
		if name in pname:
			currname = name

	if currname == 'live_backing':
		orgdata[str(x)]['log'] = d[c][pname][-1]
	elif currname == 'battery-before':
		orgdata[str(x)]['battery-before'] = d[c][pname]
	else:
		orgdata[str(x)]['battery-after'] = d[c][pname]

st_matcher = re.compile(r"\[taskcluster\s+(.*)\]")
start_times = []
charge_levels = []
for trial, trial_info in orgdata.items():
	st = st_matcher.findall(trial_info['log'])[0]
	cl = None
	for line in trial_info['battery-after']:
		if 'level:' not in line:
			continue
		cl = int(line.split('level: ')[-1])
		break
	start_times.append(st)
	charge_levels.append(cl)

print(charge_levels)
print(start_times)

md = sorted_nicely([
	(start_times[c], charge_levels[c])
	for c,_ in enumerate(charge_levels)
])

print(md)

newmd = []
for entry in md:
	stime = entry[0]
	# '2020-02-15T05:32:08.156Z'
	ts = time.mktime(
		datetime.datetime.strptime(
			stime.split('.')[0], "%Y-%m-%dT%H:%M:%S"
		).timetuple()
	)
	newmd.append((ts, entry[1]))

print(newmd)

p2_len = len(newmd)
p2_lost = 100 - newmd[-1][1]
plt.scatter(
	[((ts-newmd[0][0])/60)/60 for ts, cl in newmd],
	[cl for ts, cl in newmd],
	color='r'
)

plt.axhline(35, color='black')
plt.ylim([0,100])

plt.title(
	"Battery percent over time, Points (lost) - MotoG5: %s (%s), Pixel2: %s (%s)" %
	(mg_len, mg_lost, p2_len, p2_lost)
)
plt.xlabel("Time (hours)")
plt.ylabel("Charge Level (%)")
plt.legend(('Min. Charge', 'Moto G5', 'Pixel 2'))

"""

P2 - BREAKDOWN

"""

# CL is the starting charge, time to charge is
# from the end of previous task to start of current.


# Organize the data
orgdata = {}

d = data[0]['data']
xaxis = data[0]['xaxis']
for c, x in enumerate(xaxis):
	if str(x) not in orgdata:
		orgdata[str(x)] = {
			'log': None, 'battery-before': None, 'battery-after': None
		}

	currname = None
	pname = list(d[c].keys())[0]
	names = ['live_backing', 'battery-before', 'battery-after']
	for name in names:
		if name in pname:
			currname = name

	if currname == 'live_backing':
		orgdata[str(x)]['log'] = [d[c][pname][0], d[c][pname][-1]]
	elif currname == 'battery-before':
		orgdata[str(x)]['battery-before'] = d[c][pname]
	else:
		orgdata[str(x)]['battery-after'] = d[c][pname]

st_matcher = re.compile(r"\[taskcluster\s+(.*)\]")
durations = []
start_times = []
end_times = []
start_charge_levels = []
end_charge_levels = []
for trial, trial_info in orgdata.items():
	st = st_matcher.findall(trial_info['log'][0])[0]
	et = st_matcher.findall(trial_info['log'][1])[0]

	scl = None
	for line in trial_info['battery-before']:
		if 'level:' not in line:
			continue
		scl = int(line.split('level: ')[-1])
		break
	ecl = None
	for line in trial_info['battery-after']:
		if 'level:' not in line:
			continue
		ecl = int(line.split('level: ')[-1])
		break

	end_times.append(et)
	start_times.append(st)
	end_charge_levels.append(ecl)
	start_charge_levels.append(scl)

md = sorted_nicely([
	(start_times[c], end_times[c], start_charge_levels[c], end_charge_levels[c])
	for c,_ in enumerate(charge_levels)
])
newmd = []
ots = None
for entry in md:
	stime = entry[0]
	ts = time.mktime(
		datetime.datetime.strptime(
			# 				  '2020-02-15T05:32:08.156Z'
			stime.split('.')[0], "%Y-%m-%dT%H:%M:%S"
		).timetuple()
	)
	if not ots:
		ots = ts

	stime = entry[1]
	ets = time.mktime(
		datetime.datetime.strptime(
			stime.split('.')[0], "%Y-%m-%dT%H:%M:%S"
		).timetuple()
	)

	newmd.append((ts-ots, ets-ots, entry[2], entry[3]))

charge_amounts = []
for c, entry in enumerate(newmd[1:]):
	charge_amounts.append(
		(
			entry[0] - newmd[c][1],
			entry[2] - newmd[c][3]
		)
	)

plt.figure()
plt.scatter(
	[c for c,_ in charge_amounts],
	[c for _,c in charge_amounts],
)

# Show duration per charge and charge amount over time
import numpy as np

plt.figure()
plt.subplot(2,1,1)
times = np.asarray([t for t,_,_,_ in newmd[1:]])/3600
plt.scatter(
	times,
	[t for t,_ in charge_amounts],
	color='b'
)

plt.title('Time spent charging over time')
plt.ylabel('Time spent charging (sec)')

plt.subplot(2,1,2)
y1 = [t for _,_,t,_ in newmd[1:]]
plt.scatter(
	times,
	y1,
	color='r'
)
y2 = [t for _,_,_,t in newmd[1:]]
plt.scatter(
	times,
	y2,
	color='r',
	facecolors='none'
)
ax = plt.gca()
ax.fill_between(times, y1, y2)

plt.scatter(
	times,
	[t for _,t in charge_amounts],
	color='k'
)
plt.axhline(np.mean([t for _,t in charge_amounts]), color='k')
plt.axhline(35, color='k', linestyle='--')

plt.legend(('Avg. Charge Amount', 'Min. Charge', 'Start %', 'End %', 'Discharged Amount', 'Charged Amount'))
plt.title('Charge level over time')
plt.xlabel('Time (hours)')
plt.ylabel('Charge %')
plt.suptitle("Pixel 2 Charging Information")

# Get average charge time before first time we hit under 35%, and
# average after we hit it.
before = []
after = []
hit35 = False
for c, e in enumerate(newmd[1:]):
	if charge_amounts[c][0] > 400:
		continue
	if e[3] <= 35:
		after.append(charge_amounts[c][0])
	else:
		before.append(charge_amounts[c][0])

b_avgdurr = np.mean(before)
a_avgdurr = np.mean(after)

print("Average charge duration before first 35% hit: {}".format(b_avgdurr))
print("Average charge duration after first 35% hit: {}".format(a_avgdurr))
print("Percentage increase: {}".format((a_avgdurr-b_avgdurr)/b_avgdurr))

# plt.show()


"""

MOTOG5 Breakdown

"""

# Open the data
android_data = 'battery_tracking.json'
with open(android_data, 'r') as f:
	data = json.load(f)

# Organize the data
orgdata = {}

d = data[0]['data']
xaxis = data[0]['xaxis']
for c, x in enumerate(xaxis):
	if str(x) not in orgdata:
		orgdata[str(x)] = {
			'log': None, 'battery-before': None, 'battery-after': None
		}

	currname = None
	pname = list(d[c].keys())[0]
	names = ['live_backing', 'battery-before', 'battery-after']
	for name in names:
		if name in pname:
			currname = name

	if currname == 'live_backing':
		orgdata[str(x)]['log'] = [d[c][pname][0], d[c][pname][-1]]
	elif currname == 'battery-before':
		orgdata[str(x)]['battery-before'] = d[c][pname]
	else:
		orgdata[str(x)]['battery-after'] = d[c][pname]

st_matcher = re.compile(r"\[taskcluster\s+(.*)\]")
durations = []
start_times = []
end_times = []
start_charge_levels = []
end_charge_levels = []
for trial, trial_info in orgdata.items():
	st = st_matcher.findall(trial_info['log'][0])[0]
	et = st_matcher.findall(trial_info['log'][1])[0]

	scl = None
	for line in trial_info['battery-before']:
		if 'level:' not in line:
			continue
		scl = int(line.split('level: ')[-1])
		break
	ecl = None
	for line in trial_info['battery-after']:
		if 'level:' not in line:
			continue
		ecl = int(line.split('level: ')[-1])
		break

	end_times.append(et)
	start_times.append(st)
	end_charge_levels.append(ecl)
	start_charge_levels.append(scl)

md = sorted_nicely([
	(start_times[c], end_times[c], start_charge_levels[c], end_charge_levels[c])
	for c,_ in enumerate(end_charge_levels)
])
newmd = []
ots = None
for entry in md:
	stime = entry[0]
	ts = time.mktime(
		datetime.datetime.strptime(
			# 				  '2020-02-15T05:32:08.156Z'
			stime.split('.')[0], "%Y-%m-%dT%H:%M:%S"
		).timetuple()
	)
	if not ots:
		ots = ts

	stime = entry[1]
	ets = time.mktime(
		datetime.datetime.strptime(
			stime.split('.')[0], "%Y-%m-%dT%H:%M:%S"
		).timetuple()
	)

	newmd.append((ts-ots, ets-ots, entry[2], entry[3]))

charge_amounts = []
for c, entry in enumerate(newmd[1:]):
	charge_amounts.append(
		(
			entry[0] - newmd[c][1],
			entry[2] - newmd[c][3]
		)
	)

plt.figure()
plt.scatter(
	[c for c,_ in charge_amounts],
	[c for _,c in charge_amounts],
)

# Show duration per charge and charge amount over time
import numpy as np

plt.figure()
plt.subplot(2,1,1)
times = np.asarray([t for t,_,_,_ in newmd[1:]])/3600
plt.scatter(
	times,
	[t for t,_ in charge_amounts],
	color='b'
)

plt.title('Time spent charging over time')
plt.ylabel('Time spent charging (sec)')

plt.subplot(2,1,2)
y1 = [t for _,_,t,_ in newmd[1:]]
plt.scatter(
	times,
	y1,
	color='r'
)
y2 = [t for _,_,_,t in newmd[1:]]
plt.scatter(
	times,
	y2,
	color='r',
	facecolors='none'
)
ax = plt.gca()
ax.fill_between(times, y1, y2)

plt.scatter(
	times,
	[t for _,t in charge_amounts],
	color='k'
)
plt.axhline(np.mean([t for _,t in charge_amounts]), color='k')
plt.axhline(35, color='k', linestyle='--')

plt.legend(('Avg. Charge Amount', 'Min. Charge', 'Start %', 'End %', 'Discharged Amount', 'Charged Amount'))
plt.title('Charge level over time')
plt.xlabel('Time (hours)')
plt.ylabel('Charge %')
plt.suptitle("Moto G5 Charging Information")

plt.show()
