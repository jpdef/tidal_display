import numpy as np
import gtk
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter, date2num
from scipy.interpolate import interp1d
from datetime import datetime
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas

#
# New Window Stuff
#
class MainWin:
    def my_timer(self):
        self.ax1.axvline(x=date2num(self.now),color='r')

        return True# do ur work here, but not for long


    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.destroy)
        self.window.set_default_size(500,500)
        gtk.timeout_add(10, self.my_timer) # call every min
       
        fig = Figure()
        fig.set_facecolor('black')
        self.ax1 = fig.add_subplot(111)
        self.ax1.patch.set_facecolor('black')
        self.ax1.grid(True,color='white')
        for child in self.ax1.get_children():
          if isinstance(child, matplotlib.spines.Spine):
              child.set_color('#dddddd')
        self.ax1.tick_params(axis='x', colors='red')
        self.ax1.tick_params(axis='y', colors='red')

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
        self.now = datetime.now();
        now_index = 0
        week_time_array = []
        week_tide_array = []
        for i in xrange(0,len(time_array)):
            if self.now.date() == time_array[i].date():
                now_index=i; 
        print time_array[now_index]
        
        for i in xrange(now_index-5,now_index+5):
            week_time_array.append(time_array[i])
            week_tide_array.append(tide_array[i])
        
        
        #Convert dates interpolate and plot
        dates = date2num(week_time_array)
        f = interp1d(dates,week_tide_array,kind ='cubic')
        dates_new = np.linspace(dates[0],dates[len(dates)-1],num=400)
        self.ax1.plot_date(dates_new,f(dates_new),'c-')
        self.ax1.fmt_xdata = DateFormatter('%Y')
        fig.autofmt_xdate()
        canvas = FigureCanvas(fig)
        self.window.add(canvas)
        self.window.show_all()

    def main(self):
        gtk.main()



MainWin().main()

