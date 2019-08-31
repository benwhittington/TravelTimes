from key import key
import numpy as np
import csv
import requests

def get_call_string(file_name):

    with open(file_name,'r') as f:
        reader=csv.reader(f)
        data=list(reader)

    data=data[1:]
    addresses=[]
    call_string=""

    for obs in data:
        address=obs[:-3][0].replace(" ","+")
        address=address.replace(",","")
        addresses.append(address)
        call_string=call_string+address+"|"

    return addresses,call_string[:-1] # slice off last pipe

def call_maps(addresses,call_string):

    empty_request="https://maps.googleapis.com/maps/api/distancematrix/json?origins={}&destinations={}:&key={}"

    times=np.zeros([len(addresses),len(addresses)])

    for i,ad in enumerate(addresses):
        print("Getting address {}".format(i))
        request=empty_request.format(ad,call_string,key)
        result=requests.get(request).json()

        for j in range(len(addresses)):
            times[i,j]=result["rows"][0]["elements"][j]["duration"]["value"]/60

    np.savetxt("travel_times.csv",times,fmt="%3.5f", delimiter=",")

if __name__=="__main__":

    file_name="addresses.csv"

    addresses,call_string=get_call_string(file_name)

    call_maps(addresses,call_string)