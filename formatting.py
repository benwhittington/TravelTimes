import numpy as np
import csv

def read(file_name):

    depot='10 Panorama Rd, Mount Wellington, Auckland 1060, New Zealand' # depot location
    depot_start=[depot]+['depot', 'depot', 'depot']
    depot_end=[depot]+['depot', 'depot', 'depot']

    with open(file_name,'r') as f:
        reader=csv.reader(f)
        data=list(reader)[1:]

    data=np.array([depot_start]+data+[depot_end])

    return data

def job_times(data):
    data=data[:,1:]
    start_times={"am":120,"pm":360,"depot":0}
    finish_times={"am":360,"pm":600,"depot":600}

    min_start=[]
    max_start=[]

    for ad in data:
        min_start.append(start_times[ad[0]])
        max_start.append(finish_times[ad[0]])
    
    np.savetxt("min_start_time.txt",np.array(min_start),fmt="%i")
    np.savetxt("max_start_time.txt",np.array(max_start),fmt="%i")

def dow(data):
    weekHalf={"1st":[1,1,1,0,0],"2nd":[0,0,1,1,1],"depot":[1,1,1,1,1]}

    dow=[]

    for ad in data:
        dow.append(weekHalf[ad[2]])

    np.savetxt("day_of_week.txt",np.array(dow),fmt="%i")

def addresses(data):
    ads=[]
    for ad in data:
        ads.append(ad[0].replace(" ","_").replace(",","")[:-26]) # strip _Auckland_<post code>_New_Zealand

    np.savetxt("address_names_underscored_stripped.txt",np.array(ads),fmt="%s")

def duration(data):
    jobType={"short":90,"long":180,"depot":0}

    dur=[]

    for ad in data:
        dur.append(jobType[ad[3]])

    np.savetxt("job_lengths.txt",np.array(dur),fmt="%s")

if __name__=="__main__":
    data=read("addresses.csv")
    # job_times(data)
    addresses(data)
    # dow(data)
    # duration(data)

    