import csv
import statistics as stat
from scipy.signal import find_peaks
import os

#####Think about the characteristics for machine learning
#####add functions below

def Find_uuid_data_and_time(f):#####  find uuid of thingy
    data = []
    time = []
    for row in f.readlines():
        if 'uuid' in row:
            uuid = row.split()[1].split('"')[3]
        if 'TVOC' in row:
            data.append(int(row.split(',')[1]))
            time.append(row.split(',')[2].replace('\n', ''))
    return uuid,data,time



def devide(data,time,start_time):
    flag = 0
    count = -1
    count_dev = 0
    data_dev = [[],[],[],[]]
    time_dev = [[],[],[],[]]
    start_time = start_time.split(':')
    start_time = int(start_time[-1])+int(start_time[-2])*60+int(start_time[-3])*3600
    for t in time:
        count += 1
        if flag == 0:
            flag = 1
            data_dev[count_dev].append(data[count])
            time_dev[count_dev].append(int(time[count].split(':')[-1])+int(time[count].split(':')[-2])*60+int(time[count].split(':')[-3])*3600-start_time)
        else:
            B=t.split(':')
            B = int(B[-1])+int(B[-2])*60+int(B[-3])*3600
            if B - start_time > 300*(count_dev+1) or count == len(time)-1:
                flag = 0
                count_dev += 1
                if count_dev == 4:
                    break
                continue
            else :
                data_dev[count_dev].append(data[count])
                time_dev[count_dev].append(int(time[count].split(':')[-1])+int(time[count].split(':')[-2])*60+int(time[count].split(':')[-3])*3600-start_time)         
   
    return data_dev,time_dev

def Find_max_min_avg_median(data):
    dmax = max(map(int,data))
    dmin = min(map(int,data))
    davg = (dmax+dmin)/2
    dmedian = stat.median(map(int,data))
    return dmax,dmin,davg,dmedian

def Find_time(value,data,time):
    timevalue = []
    timelist = []
    for i in range(len(value)):
        for j in range(len(data)):
            if data[j] == value[i]:
                timevalue.append(time[j])
        timelist.append(timevalue)
    return timelist

def Find_var(data):  ## find variance
    var = stat.pvariance(map(int,data))
    return var

def Find_time_interval(timeA,timeB):
    A=timeA.split(':')
    B=timeB.split(':')
    A = int(A[-1])+int(A[-2])*60+int(A[-3])*3600
    B = int(B[-1])+int(B[-2])*60+int(B[-3])*3600  
    if(A>B):
        interval = A-B
    else:
        interval = B-A
    return interval


## find no of peaks, their value and time(even though multiple peaks should not happen)
def Find_peaks_and_prominence(data,time,davg):
    
    peak_id,peaks_property = find_peaks(data,height = davg,threshold = None, distance = 50, prominence = davg/2, width =10, wlen = None,rel_height =0.5, plateau_size = None)
    value = 0
    timelist = 0
    prominence = 0
    for i in range(len(peak_id)):
        if data[peak_id[i]] > value:
            value = data[peak_id[i]]
            timelist = time[peak_id[i]]
            prominence = peaks_property["prominences"][i]
    
    return value,timelist,prominence


## data processing for 1 file
def Find_char(filename,start_time):
    with open(filename, 'r') as f:
        uuid,data,time = Find_uuid_data_and_time(f)
    data_dev, time_dev = devide(data,time,start_time)

    dmax = [0] * 4
    dmin = [0] * 4
    davg = [0] * 4
    dmedian = [0] * 4
    peak_values= [0] * 4
    peak_times= [0] * 4
    prominence= [0] * 4
    dvar = [0] * 4
    for i in range(0,4):
        
        dmax[i],dmin[i],davg[i],dmedian[i] = Find_max_min_avg_median(data_dev[i])
        peak_values[i],peak_times[i],prominence[i] = Find_peaks_and_prominence(data_dev[i],time_dev[i],davg[i])
        dvar[i] = Find_var(data_dev[i])


    #get region
    region = filename.split('/')[5]
    location_x = filename.split('/')[6].split('_')[2]
    location_y = filename.split('/')[6].split('_')[3]
    f.close
    export(uuid,dmax,dmin,davg,dmedian,peak_values,peak_times,prominence,dvar,region,location_x,location_y)
        

##data processing for 3 files
def export(uuid,dmax,dmin,davg,dmedian,peak_values,peak_times,prominence,dvar,region,location_x,location_y):
    with open('all_1.csv', mode='a',newline='') as overall_file:
        fieldnames = ['sensor',
                      'dmax1','dmin1','davg1','dmedian1','peak_values1','peak_times1','prominence1','dvar1',
                      'dmax2','dmin2','davg2','dmedian2','peak_values2','peak_times2','prominence2','dvar2',
                      'dmax3','dmin3','davg3','dmedian3','peak_values3','peak_times3','prominence3','dvar3',
                      'dmax4','dmin4','davg4','dmedian4','peak_values4','peak_times4','prominence4','dvar4',
                      'Region','Location_x','Location_y']
        writer = csv.DictWriter(overall_file, fieldnames=fieldnames)
        writer.writerow({'sensor':uuid,
                         'dmax1':dmax[0],'dmin1':dmin[0],'davg1':davg[0],'dmedian1':dmedian[0],
                         'peak_values1':peak_values[0],'peak_times1':peak_times[0],'prominence1':prominence[0],'dvar1':dvar[0],
                         'dmax2':dmax[1],'dmin2':dmin[1],'davg2':davg[1],'dmedian2':dmedian[1],
                         'peak_values2':peak_values[1],'peak_times2':peak_times[1],'prominence2':prominence[1],'dvar2':dvar[1],
                         'dmax3':dmax[2],'dmin3':dmin[2],'davg3':davg[2],'dmedian3':dmedian[2],
                         'peak_values3':peak_values[2],'peak_times3':peak_times[2],'prominence3':prominence[2],'dvar3':dvar[2],
                         'dmax4':dmax[3],'dmin4':dmin[3],'davg4':davg[3],'dmedian4':dmedian[3],
                         'peak_values4':peak_values[3],'peak_times4':peak_times[3],'prominence4':prominence[3],'dvar4':dvar[3],
                         'Region':region,'Location_x':location_x,'Location_y':location_y })
    overall_file.close
    return   

#read all files
def read_all_files(directory):
    entries = os.listdir(directory)


    for foldernames in entries:
        subfolder = os.listdir(directory+'/'+ str(foldernames))
        print(foldernames)
        for subfoldernames in subfolder:
            files= os.listdir(directory+'/'+ str(foldernames)+'/'+ str(subfoldernames))
            flag = 0
            for filenames in files:
                if flag == 0:
                    with open (directory+'/'+ str(foldernames)+'/'+ str(subfoldernames)+'/'+str(filenames),'r') as f:
                        uuid, data, time = Find_uuid_data_and_time(f)
                    start_time = time [0]
                    flag = 1
                    f.close
                    
                Find_char(directory+'/'+ str(foldernames)+'/'+ str(subfoldernames)+'/'+str(filenames),start_time)

    return
    




def modify(filename):
    new_row =[0]*102
    with open(filename,'r')as f1:
        with open('all_2.csv', mode='a',newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            flag = 0
            
            for row in f1.readlines():
                uuid = row.split(',')[0]
                if uuid == 'e2c84430970e':
                    new_row[0:33] = row.split(',')[0:33]
                elif uuid == 'e062039dd423':
                    new_row[33:66] = row.split(',')[0:33]
                else:
                    
                    new_row[66:101] = row.split(',')[0:35]
                    new_row[101] = int(row.split(',')[35])
                    
                flag +=1
                if flag == 3:
                    flag =0
                    writer.writerow(new_row)
                    new_row = [0]*102
        csvfile.close
    f1.close
    return

def compare(filename):
    with open(filename, 'r') as f:
        with open('all_3.csv', mode='a',newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in f.readlines():
                
                row = row.split(',')
                row[len(row)-1] = int(row[len(row)-1])
                compare_avg_ab1 = float(row[3])-float(row[36])
                compare_avg_bc1 = float(row[36])-float(row[69])
                compare_avg_ca1 = float(row[69])-float(row[3])
                
                compare_avg_ab2 = float(row[11])-float(row[44])
                compare_avg_bc2 = float(row[44])-float(row[77])
                compare_avg_ca2 = float(row[77])-float(row[11])
                
                compare_avg_ab3 = float(row[19])-float(row[52])
                compare_avg_bc3 = float(row[52])-float(row[85])
                compare_avg_ca3 = float(row[85])-float(row[19])
                
                compare_avg_ab4 = float(row[27])-float(row[60])
                compare_avg_bc4 = float(row[60])-float(row[93])
                compare_avg_ca4 = float(row[93])-float(row[27])
                
                compare_max_ab1 = float(row[1])-float(row[34])
                compare_max_bc1 = float(row[34])-float(row[67])
                compare_max_ca1 = float(row[67])-float(row[1])
                
                compare_max_ab2 = float(row[9])-float(row[42])
                compare_max_bc2 = float(row[42])-float(row[75])
                compare_max_ca2 = float(row[75])-float(row[9])
                
                compare_max_ab3 = float(row[17])-float(row[50])
                compare_max_bc3 = float(row[50])-float(row[83])
                compare_max_ca3 = float(row[83])-float(row[17])
                
                compare_max_ab4 = float(row[25])-float(row[58])
                compare_max_bc4 = float(row[58])-float(row[91])
                compare_max_ca4 = float(row[91])-float(row[25])

                row.append(compare_avg_ab1)
                row.append(compare_avg_bc1)
                row.append(compare_avg_ca1)
                row.append(compare_avg_ab2)
                row.append(compare_avg_bc2) 
                row.append(compare_avg_ca2)
                
                row.append(compare_avg_ab3)
                row.append(compare_avg_bc3)
                row.append(compare_avg_ca3)
                
                row.append(compare_avg_ab4)
                row.append(compare_avg_bc4)
                row.append(compare_avg_ca4)
                
                row.append(compare_max_ab1)
                row.append(compare_max_bc1)
                row.append(compare_max_ca1)
                
                row.append(compare_max_ab2)
                row.append(compare_max_bc2)
                row.append(compare_max_ca2)
                
                row.append(compare_max_ab3)
                row.append(compare_max_bc3)
                row.append(compare_max_ca3)
                
                row.append(compare_max_ab4)
                row.append(compare_max_bc4)
                row.append(compare_max_ca4)

                writer.writerow(row)

            csvfile.close
        f.close
    return
            
                    
                    
            
          
            
        


