import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.dates import DateFormatter, date2num
from scipy.interpolate import interp1d
from datetime import datetime

#Intialize plotting tools
#plt.ion is iterative fn

fig ,ax1 = plt.subplots()
ax1.set_axis_bgcolor('black')
fig.tight_layout()
plt.ion()

#Open file parse into arrays
tide_data = open('tide_data.txt','r')
time_array = []
tide_array = []

#runs through file by line inserts in array
#parse based on time and tide level
i =0
for line in tide_data:
    s = line.split()
    time_array.append( datetime.strptime(s[0] + " " + s[2] + " " + s[3],
    "%Y/%m/%d %I:%M %p") )
    tide_array.append(float(s[4]) )


#Finds current week so graph displays
#current data
now = datetime.now();
now_index = 0
week_time_array = []
week_tide_array = []
for i in xrange(0,len(time_array)):
    if now.date() == time_array[i].date():
        now_index=0; 

for i in xrange(now_index,now_index+40):
    week_time_array.append(time_array[i])
    week_tide_array.append(tide_array[i])

#Convert dates interpolate and plot
dates = date2num(week_time_array)
f = interp1d(dates,week_tide_array,kind ='cubic')
dates_new = np.linspace(dates[0],dates[len(dates)-1],num=400)
ax1.plot_date(dates_new,f(dates_new),'b-')
ax1.fmt_xdata = DateFormatter('%Y')
fig.autofmt_xdate()
plt.show()

#update on time marker
while True:
   ax1.plot_date(np.repeat(date2num(now),20),np.arange(-10,10),'r-')
   plt.draw()
