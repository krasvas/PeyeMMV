#	PeyeMMV: Python implementation of EyeMMV’s fixation detection algorithm
#	Copyright (C) 2022 Vassilios Krassanakis (University of West Attica)

#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.

#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.

#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.

#	For further information, please email me: krasvas[at]uniwa[dot]gr

from statistics import mean
from math import sqrt
import matplotlib.pyplot as plt
import itertools

# PeyeMMV parameters:
# file: raw gaze data (x,y,passing time)
# t1,t2: spatial parameters for fixation identification
# min_dur: minimum duration threshold for fixation identification
# report_fix: selecting the value '1', raw gaze data and fixation plot is generated
# Run example (after importing peyemmv module): peyemmv.extract_fixations('demo_data.txt',0.25,0.1,150,'1')

def extract_fixations(file,t1,t2,min_dur,report_fix):
  
	# Define Euclidean distance between two points
    def dist2p(x1,y1,x2,y2):
        dx=x2-x1
        dy=y2-y1
        return (sqrt((dx**2)+(dy**2)))
	
    # Read raw data file
    data=open(file,'r')

    # Initialize x,y,t,p(x,y,t)
    x=[]
    y=[]
    t=[]
    p=[]

    # Initialize fixation cluster and fixations list
    fix_clust=[]
    fix_clust_t2=[]
    x_t2=[]
    y_t2=[]
    t_t2=[]

    x_gaze=[]
    y_gaze=[]
    t_gaze=[]
    fixations=[]

    for line in data:
        line=line.split()
        #append x,y,t values
        x.append(float(line[0]))
        y.append(float(line[1]))
        t.append(float(line[2]))
        p.append([float(line[0]),float(line[1]),float(line[2])])

    # Initialize fixation mean point
    fixx=x[0]
    fixy=y[0]
        
    for point in p:
        dist=dist2p(fixx,fixy,point[0],point[1])
        
        #check spatial threshold
        if dist<t1:
            x_gaze.append(point[0])
            y_gaze.append(point[1])
            t_gaze.append(point[2])
            fixx=mean(x_gaze)
            fixy=mean(y_gaze)
                    
        else:
            # Put all gaze points in a fixation cluster
            fix_clust.append([x_gaze,y_gaze,t_gaze])
            if len(fix_clust[0][0])>=1:
                fixx_clust=mean(fix_clust[0][0])
                fixy_clust=mean(fix_clust[0][1])
                
                for (xg,yg,tg) in zip(fix_clust[0][0],fix_clust[0][1],fix_clust[0][2]):
                    if dist2p(fixx_clust,fixy_clust,xg,yg)<t2:
                        x_t2.append(xg)
                        y_t2.append(yg)
                        t_t2.append(tg)
                        
                fixx_clust_t2=mean(x_t2)
                fixy_clust_t2=mean(y_t2)
                fixdur_clust_t2=t_t2[-1]-t_t2[0]
                                    
                # Check minimum duration threshold
                if fixdur_clust_t2>=min_dur:
                    #mean_x,mean_y,dur,start,end
                    fixations.append([fixx_clust_t2,fixy_clust_t2,fixdur_clust_t2,t_t2[0],t_t2[-1],len(t_t2)])
                    
            # Initialize fixation mean point and gaze points
            fixx=point[0]
            fixy=point[1]
            x_gaze=[]
            y_gaze=[]
            t_gaze=[]
            fix_clust=[]
            fix_clust_t2=[]
            x_t2=[]
            y_t2=[]
            t_t2=[]
                
    # Generate fixation report (plot values)  
    if report_fix=='1':
        #print final fixations
        x_fix=[]
        y_fix=[]
        dur_fix=[]
        print("Fixation_ID [X_coord, Y_coord, Duration, Start_time, End_time, No_gaze_points]")
        
        # Define a fixation counter
        fix_count=0
        for fix in fixations:
            fix_count=fix_count+1
            print (fix_count,fix)
            x_fix.append(fix[0])
            y_fix.append(fix[1])
            dur_fix.append(fix[2])
        
        plt.title("Fixation points")
        plt.xlabel("Horizontal coordinates (tracker units)")
        plt.ylabel("Vertical coordinates (tracker units)")
    
        plt.scatter(x,y,color='blue',marker='+')
        plt.scatter(x_fix,y_fix,color='red',marker='.')
        plt.legend(['raw gaze data','fixation centers and their durations'],loc='best')
        for i in range(len(x_fix)):   
            plt.text(x_fix[i],y_fix[i],"{:.1f}".format(dur_fix[i]),color='red')
        plt.grid()
        plt.show()
    else:
        pass

    return(fixations)
