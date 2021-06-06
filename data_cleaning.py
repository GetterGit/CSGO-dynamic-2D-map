import json
import re

fh=open('round_data_full.txt')
data=fh.read()
#creating a new object to then keep updating it in the loops below, otherwise the scripts always take the initial data and disregard the progress
data_new=data


#the parameter name doesn't contain _ and there's a comma after its value
flaw_1=re.findall('"[a-z]+": [0-9]+,', data)
for f in flaw_1: 
	f_new=f[0:f.find(':')+1]+' "'+f[f.find(':')+2:len(f)-1]+'"'+','
	data_new=re.sub(f, f_new, data_new)

#the parameter name contains _ and there's a comma after its value
flaw_2=re.findall('"[a-z]+_[a-z]+": [0-9]+,', data)
for f in flaw_2: 
	f_new=f[0:f.find(':')+1]+' "'+f[f.find(':')+2:len(f)-1]+'"'+','
	data_new=re.sub(f, f_new, data_new)

#the parameter name doesn't contain _ and there's no comma after its value
flaw_3=re.findall('"[a-z]+": [0-9]+', data)
for f in flaw_3: 
	f_new=f[0:f.find(':')+1]+' "'+f[f.find(':')+2:]+'"'
	data_new=re.sub(f, f_new, data_new)

#the parameter name contains _ and there's no comma after its value
flaw_4=re.findall('"[a-z]+_[a-z]+": [0-9]+', data)
for f in flaw_4: 
	f_new=f[0:f.find(':')+1]+' "'+f[f.find(':')+2:]+'"'
	data_new=re.sub(f, f_new, data_new)

#the parameter name contains _ and the value is a string/True/False without comma at the end
flaw_5=re.findall('"[a-z]+_[a-z]+": [a-z]+', data)
for f in flaw_5: 
	f_new=f[0:f.find(':')+1]+' "'+f[f.find(':')+2:]+'"'
	data_new=re.sub(f, f_new, data_new)

#the parameter name doesn't contain _ and the value is a string/True/False without comma at the end
flaw_6=re.findall('"[a-z]+": [a-z]+', data)
for f in flaw_6: 
	f_new=f[0:f.find(':')+1]+' "'+f[f.find(':')+2:]+'"'
	data_new=re.sub(f, f_new, data_new)

#the parameter name doesn't contain _ and the value is a string/True/False with comma at the end
flaw_7=re.findall('"[a-z]+": [a-z]+,', data)
for f in flaw_7: 
	f_new=f[0:f.find(':')+1]+' "'+f[f.find(':')+2:len(f)-1]+'"'+','
	data_new=re.sub(f, f_new, data_new)

#the parameter name contains _ and the value is a string/True/False with comma at the end
flaw_8=re.findall('"[a-z]+_[a-z]+": [a-z]+,', data)
for f in flaw_8: 
	f_new=f[0:f.find(':')+1]+' "'+f[f.find(':')+2:len(f)-1]+'"'+','
	data_new=re.sub(f, f_new, data_new)	

#the parameter name contains _ x 2 and with comma at the end
flaw_9=re.findall('"[a-z]+_[a-z]+_[a-z]+": [0-9]+,', data)
for f in flaw_9: 
	f_new=f[0:f.find(':')+1]+' "'+f[f.find(':')+2:len(f)-1]+'"'+','
	data_new=re.sub(f, f_new, data_new)	

#the parameter name contains _ x 3 and with comma at the end
flaw_10=re.findall('"[a-z]+_[a-z]+_[a-z]+_[a-z]+": [0-9]+,', data)
for f in flaw_10: 
	f_new=f[0:f.find(':')+1]+' "'+f[f.find(':')+2:len(f)-1]+'"'+','
	data_new=re.sub(f, f_new, data_new)	

#the parameter name contains _ x 2 and without comma at the end
flaw_11=re.findall('"[a-z]+_[a-z]+_[a-z]+": [0-9]+', data)
for f in flaw_11: 
	f_new=f[0:f.find(':')+1]+' "'+f[f.find(':')+2:]+'"'
	data_new=re.sub(f, f_new, data_new)	

#the parameter name contains _ x 3 and without comma at the end
flaw_12=re.findall('"[a-z]+_[a-z]+_[a-z]+_[a-z]+": [0-9]+', data)
for f in flaw_12: 
	f_new=f[0:f.find(':')+1]+' "'+f[f.find(':')+2:]+'"'
	data_new=re.sub(f, f_new, data_new)	

#the parameter name contains _ x 4 and withoutout comma at the end
flaw_13=re.findall('"[a-z]+_[a-z]+_[a-z]+_[a-z]+_[a-z]+": [0-9]+', data)
for f in flaw_13: 
	f_new=f[0:f.find(':')+1]+' "'+f[f.find(':')+2:]+'"'
	data_new=re.sub(f, f_new, data_new)	

#the parameter name contains _ x 4 and with comma at the end
flaw_14=re.findall('"[a-z]+_[a-z]+_[a-z]+_[a-z]+": [0-9]+,', data)
for f in flaw_14: 
	f_new=f[0:f.find(':')+1]+' "'+f[f.find(':')+2:len(f)-1]+'"'+','
	data_new=re.sub(f, f_new, data_new)	

print(data_new)


