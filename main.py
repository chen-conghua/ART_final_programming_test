import numpy as np

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

  	
def imu(imu_l, min_t):
	with open(IMUfile, 'w') as f:
		f.write('')
	temp_l = []
	acce = ['0', '0', '0']
	gyro = ['0', '0', '0']
	magnf, magnb = [0, 0, 0], [0, 0, 0]
	ahrsf, ahrsb = [0, 0, 0], [0, 0, 0]
	presf, presb = 0, 0
	count = 1
	for i in imu_l:
		temp_l = []
		if i[0] == 'PRES':
			presf = presb
			presb = float(i[3])
			pres_array = np.linspace(presf, presb, 39)
		elif i[0] == 'ACCE':
			acce[0] = i[3]
			acce[1] = i[4]
			acce[2] = i[5]
		elif i[0] == 'GYRO':
			gyro[0] = i[3]
			gyro[1] = i[4]
			gyro[2] = i[5]
		elif i[0] == 'MAGN':
			magnf[0] = magnb[0]
			magnf[1] = magnb[1]
			magnf[2] = magnb[2]
			magnb[0] = i[3]
			magnb[1] = i[4]
			magnb[2] = i[5]
			magn_array0 = np.linspace(float(magnf[0]), float(magnb[0]), 2)
			magn_array1 = np.linspace(float(magnf[1]), float(magnb[1]), 2)
			magn_array2 = np.linspace(float(magnf[2]), float(magnb[2]), 2)
		elif i[0] == 'AHRS':
			ahrsf[0] = ahrsb[0]
			ahrsf[1] = ahrsb[1]
			ahrsf[2] = ahrsb[2]
			ahrsb[0] = i[3]
			ahrsb[1] = i[4]
			ahrsb[2] = i[5]
			ahrs_array0 = np.linspace(float(ahrsf[0]), float(ahrsb[0]), 2)
			ahrs_array1 = np.linspace(float(ahrsf[1]), float(ahrsb[1]), 2)
			ahrs_array2 = np.linspace(float(ahrsf[2]), float(ahrsb[2]), 2)


		if presf == 0:
			continue

		if i[0] == 'ACCE':
			temp_l.append(str(int(float(i[2]) * 1000) - int(min_t * 1000)))
			temp_l.append(acce[0])
			temp_l.append(acce[1])
			temp_l.append(acce[2])
			temp_l.append(gyro[0])
			temp_l.append(gyro[1])
			temp_l.append(gyro[2])
			temp_l.append( str(magn_array0[count % 2]))
			temp_l.append( str(magn_array1[count % 2]))
			temp_l.append( str(magn_array2[count % 2]))
			temp_l.append( str(ahrs_array0[count % 2]))
			temp_l.append( str(ahrs_array1[count % 2]))
			temp_l.append( str(ahrs_array2[count % 2]))
			temp_l.append(str(pres_array[count]))
			
			count += 1
			if count >= 39:
  				count = 0

		with open(IMUfile, 'a+') as f:
			f.writelines(','.join(temp_l) + '\n')
			



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

imu(imu_list, min_imu_tim)
wifi(wifi_list, min_wifi_tim)
gnss(gnss_list)