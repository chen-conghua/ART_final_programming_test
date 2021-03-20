
originfilename = "logfile_2020_03_19_09_31_56.txt"
IMUfile = 'imu.txt'
WIFIfile = 'wifi.txt'
GNSSfile = 'gnss.txt'

imu_list = []
wifi_list = []
gnss_list = []
min_imu_tim = float('inf')
min_wifi_tim = float('inf')
min_gnss_tim = float('inf')

#计算mac地址转化为整数
def macstr_to_int(mac_str):
	sum = 0
	count = 11
	for i in mac_str:
		if ord(i) >= 48 and ord(i) <=57:
  			sum = (sum + int(i)) * (16 ** count)
		elif ord(i) >= 97 and ord(i) <= 102:
  			sum = (sum + (ord(i) - 87)) * (16 ** count)
		count -= 1
		return str(sum)
  			
  	
def imu():
	with open(IMUfile, 'w') as f:
		f.write('')
	


#处理wifi，wifi_l列表，min_t为最小时间
def wifi(wifi_l,min_t):
	with open(WIFIfile, 'w') as f:
				f.write('')
	for l in wifi_l:
		temp_l = []
		temp_l.append(str(int((float(l[2])-min_t)*1000))) #待改
		temp_l.append(macstr_to_int(l[4].replace(':', '')))
		if len(l) == 7:
			temp_l.append(l[6])
		elif len(l) == 6:
			temp_l.append(l[5])

		with open(WIFIfile, 'a') as f:
				f.write(','.join(temp_l) + '\n')


#处理GNSS
def gnss(gnss_l):
	with open(GNSSfile, 'w') as f:
				f.write('')
	temp_l = []
	for g in gnss_l:
		temp_l.append(g[1])
		temp_l.append(g[2])
		temp_l.append(g[3])
		temp_l.append(g[4])
		temp_l.append(g[5])
		temp_l.append(g[6])
		temp_l.append(g[7])
		temp_l.append(g[9])
		temp_l.append(g[10])

		with open(GNSSfile, 'a') as f:
				f.write(','.join(temp_l) + '\n')

with open(originfilename, "r") as f:
	for line in f:
		if line[0] == '%' or line[0:4] == "LIGH" or line[0:4] == "SOUN":
			continue
		else:
			if line[0:4] == "ACCE" or line[0:4] == "GYRO" or line[0:4] == "MAGN" or line[0:4] == "PRES"	 or line[0:4] == "AHRS":
				imu_t = line.strip('\n').split(';')
				if float(imu_t[2]) < min_imu_tim:
  					min_imu_tim = float(imu_t[2])
				imu_list.append(imu_t)
						
			elif line[0:4] == "WIFI":
				wifi_t = line.strip('\n').split(';')
				if float(wifi_t[2]) < min_wifi_tim:
  					min_wifi_tim = float(wifi_t[2])
				wifi_list.append(wifi_t)

			elif line[0:4] == "GNSS":
				gnss_t = line.strip('\n').split(';')
				if float(gnss_t[2]) <min_gnss_tim:
  					min_gnss_tim = float(gnss_t[2])
				gnss_list.append(gnss_t)

imu()
wifi(wifi_list, min_wifi_tim)
gnss(gnss_list)