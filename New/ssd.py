import subprocess
import pandas as pd
import datetime as ti
import time
import re

Read_IOPS = []
Read_BW = []
Write_IOPS = []
Write_BW = []

now = ti.datetime.now()
hour = int(now.hour)
minute = int(now.minute)
past = 0
time_ = []

def read_status():
	h = hour - int(now.hour)
	m = minute - int(now.minute)

	if m % 10 == 0:
		cmd_ssd = "sudo fio ssd_test.fio"
		sysMsg = subprocess.getstatusoutput(cmd_ssd)

		f = open("ssd_info.txt", 'w')
		f.write(str(sysMsg[1]))
		f.close

		with open('ssd_info.txt', 'r') as f:
		    read_BW = str(f.readlines()[16])
		    match = re.search(r'avg=\s*([^,\s]*)', read_BW)
		    if match:
		    	read_BW = float(match.group(1))
		f.close()

		with open('ssd_info.txt', 'r') as f:
		    read_IOPS = str(f.readlines()[17])
		    match = re.search(r'avg=\s*([^,\s]*)', read_IOPS)
		    if match:
		    	read_IOPS = float(match.group(1))
		f.close()

		with open('ssd_info.txt', 'r') as f:
		    write_BW = str(f.readlines()[28])
		    match = re.search(r'avg=\s*([^,\s]*)', write_BW)
		    if match:
		    	write_BW = float(match.group(1))
		f.close()

		with open('ssd_info.txt', 'r') as f:
		    write_IOPS = str(f.readlines()[29])
		    match = re.search(r'avg=\s*([^,\s]*)', write_IOPS)
		    if match:
		    	write_IOPS = float(match.group(1))
		f.close()

		t = str(h) + "-" + str(m)
		time_.append(t)
		Read_BW.append(read_BW)
		Read_IOPS.append(read_IOPS)
		Write_BW.append(write_BW)
		Write_IOPS.append(write_IOPS)
		print(Read_BW)

try:
	while True:
		now = ti.datetime.now()
		_minute = int(now.minute)
		if (past != _minute):
		    read_status()
		    past = _minute
		else:
		    pass
		


except KeyboardInterrupt:
	data = {'read_BW': Read_BW, 'read_IOPS': Read_IOPS, 'write_BW': Write_BW, 'write_IOPS': Write_IOPS, 'time': time_}
	df = pd.DataFrame(data)
	df.to_csv('_info.csv', index=False)



