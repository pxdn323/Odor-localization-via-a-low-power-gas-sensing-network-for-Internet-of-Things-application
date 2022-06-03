import csv
import os
import time
#####Think about the characteristics for machine learning
#####add functions below

def Find_uuid_data_and_time(f):#####  find uuid of thingy
    data = []
    timeli = []
    for row in f.readlines():
        if 'uuid' in row:
            uuid = row.split()[1].split('"')[3]
        if 'TVOC' in row:
            data.append(int(row.split(',')[1]))
            timei = str( row.split(',')[2].replace('\n', ''))
            timeArray = time.strptime(timei, "%Y:%m:%d:%H:%M:%S")
            timestamp = time.mktime(timeArray)
            timeli.append(timestamp)
    return uuid,data,timeli

def Find_char(filename,data1,data2,data3,timeli):

    #get region
    region = int(filename.split('/')[2].split(' ')[1])
    location_x = int(filename.split('/')[3].split('_')[2])
    location_y = int(filename.split('/')[3].split('_')[3])
    for i in range (0,len(data1)):
        export(data1[i],data2[i],data3[i],region,location_x,location_y,timeli[i])
    

##data processing for 3 files
def export(data1,data2,data3,region,location_x,location_y,timeli):
    with open('con_1.csv', mode='a',newline='') as overall_file:
        fieldnames = ['sensor1','sensor2','sensor3','region','location_x','location_y','time']
        writer = csv.DictWriter(overall_file, fieldnames=fieldnames)
        writer.writerow({'sensor1':data1,'sensor2':data2,'sensor3':data3,'region':region,'location_x':location_x,'location_y':location_y,'time':timeli})
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
                    print(filenames)
                    with open (directory+'/'+ str(foldernames)+'/'+ str(subfoldernames)+'/'+str(filenames),'r') as f:
                        uuid, data, timeli = Find_uuid_data_and_time(f)
                    #start_time = time [0]
                    #end_time = time[len(time)-1]
                    f.close

                    if uuid == 'e2c84430970e':
                        data1 = data
                        time1 = timeli
                    elif uuid == 'e062039dd423':
                        data2 = data
                        time2 = timeli
                    else:
                        data3 = data
                        time3 = timeli

            data_len = min(len(data1),len(data2),len(data3))-1
            if abs(time1[0]-time2[0]) <= 30 and abs(time2[0]-time3[0]) <= 30 and abs(time1[0]-time3[0]) <= 30 and abs(time1[data_len]-time2[data_len]) <= 30 and abs(time1[data_len]-time3[data_len]) <= 30 and abs(time3[data_len]-time2[data_len]) <= 30:
                    Find_char(directory+'/'+ str(foldernames)+'/'+ str(subfoldernames)+'/'+str(filenames),data1[0:data_len+1],data2[0:data_len+1],data3[0:data_len+1],timeli[0:data_len+1])

    return
    




def modify(filename):
    new_row =[0]*7
    with open(filename,'r')as f1:
        with open('con_2.csv', mode='a',newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            flag = 0
            
            for row in f1.readlines():
                uuid = row.split(',')[0]
                if uuid == 'e2c84430970e':
                    new_row[0] = row.split(',')[1]
                elif uuid == 'e062039dd423':
                    new_row[1] = row.split(',')[1]
                else:
                    
                    new_row[2:5] = row.split(',')[1:4]
                    new_row[6] = int(row.split(',')[5])
                    
                flag +=1
                if flag == 3:
                    flag =0
                    writer.writerow(new_row)
                    new_row = [0]*7
        csvfile.close
    f1.close
    return

