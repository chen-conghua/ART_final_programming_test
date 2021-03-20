
filename = "logfile_2020_03_19_09_31_56.txt"
imu_list = []
wifi_list = []
gnss_list = []
min_imu_tim = float('inf')
min_wifi_tim = float('inf')
min_gnss_tim = float('inf')

def imu_p():
	pass

def wifi_p():
  pass	

def gnss_p():
	pass

with open(filename, "r") as f:
	for line in f:
		if line[0] == '%':
			continue
		else:
			if line[0:4] == "ACCE" or line[0:4] == "GYRO" or line[0:4] == "MAGN" or line[0:4] == "PRES"	or line[0:4] == "LIGH" or line[0:4] == "AHRS" or line[0:4] == "SOUN":
				imu_t = line.strip('\n').split(';')
				if imu_t[2] < min_imu_tim:
  					min_imu_tim = imu_t[2]
				imu_list.append(imu_t)
						
			elif line[0:4] == "WIFI":
				wifi_t = line.strip('\n').split(';')
				if wifi_t[2] < min_wifi_tim:
  					min_wifi_tim = wifi_t[2]
				wifi_list.append(wifi_t)

			elif line[0:4] == "GNSS":
				gnss_t = line.strip('\n').split(';')
				if gnss_t[2] <min_gnss_tim:
  					min_gnss_tim = gnss_t
				gnss_list.append(gnss_t)