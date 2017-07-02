#coding: utf-8


import os
import sys
import shutil


dir ="/Users/zhanghan/Documents/文件资料/LPD/ex/deadline/L2DCT/"

dir1=dir+"/FCT/L2DCT"
dir2=dir+"/FCT1/L2DCT"
dir3=dir+"/FCT2/L2DCT"
dir4=dir+"/FCT3/L2DCT"
dir5=dir+"/FCT4/L2DCT"


files = os.listdir(dir1)




for f in files:
	if(os.path.isdir(dir1+"/"+f)==False):
		filename=os.path.basename(f)
		shutil.copy(dir1+"/"+f,dir+"/"+f)



files = os.listdir(dir2)




for f in files:
	if(os.path.isdir(dir1+"/"+f)==False):
		filename=os.path.basename(f)
		dest1= filename[:6]
		dest2= filename[7:]
		dest=""
		if(filename[6]=='0'):
			dest=dest1+'2'+dest2
			print dest
		else:
			dest=dest1+'3'+dest2
			print dest
		shutil.copy(dir1+"/"+f,dir+"/"+dest)




files = os.listdir(dir3)




for f in files:
	if(os.path.isdir(dir1+"/"+f)==False):
		filename=os.path.basename(f)
		dest1= filename[:6]
		dest2= filename[7:]
		dest=""
		if(filename[6]=='0'):
			dest=dest1+'4'+dest2
			print dest
		else:
			dest=dest1+'5'+dest2
			print dest
		shutil.copy(dir1+"/"+f,dir+"/"+dest)




files = os.listdir(dir4)




for f in files:
	if(os.path.isdir(dir1+"/"+f)==False):
		filename=os.path.basename(f)
		dest1= filename[:6]
		dest2= filename[7:]
		dest=""
		if(filename[6]=='0'):
			dest=dest1+'6'+dest2
			print dest
		else:
			dest=dest1+'7'+dest2
			print dest
		shutil.copy(dir1+"/"+f,dir+"/"+dest)




files = os.listdir(dir5)




for f in files:
	if(os.path.isdir(dir1+"/"+f)==False):
		filename=os.path.basename(f)
		dest1= filename[:6]
		dest2= filename[7:]
		dest=""
		if(filename[6]=='0'):
			dest=dest1+'8'+dest2
			print dest
		else:
			dest=dest1+'9'+dest2
			print dest
		shutil.copy(dir1+"/"+f,dir+"/"+dest)











