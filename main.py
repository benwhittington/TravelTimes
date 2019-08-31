from key import key
import numpy as np
import csv
import requests

def get_call_string(file_name):
    """ Puts addresses into format exceptable for API query

        inputs
        ------
        file_name : string
            directory of .csv of addresses to read

        returns
        ------

        addresses : list of strings
            Individual addresses in proper format

        call_string : string
            All addresses in single string formatted for API

    """

    with open(file_name,'r') as f:
        reader=csv.reader(f)
        data=list(reader)[1:]

    addresses=[]
    call_string=""

    for obs in data:
        address=obs[:-3][0].replace(" ","+") # remove am/pm job duration and week fields
        address=address.replace(",","")
        addresses.append(address)
        call_string=call_string+address+"|" # separates addresses

    return addresses,call_string[:-1] # slice off last pipe

def call_maps(addresses,call_string,fname="travel_times.csv"):
    """ Computes distance. returns n by n (n=len(addresses)) matrix of times from each address to every other address.
        Outputs matrix to travel_times.csv

        Note: 
        Distance matrix API accepts multiple destination and orgin args and will compute matrix automatically
        but this exceeds the rate limit so origin addresses are looped over individually and destinations
        are put in all at once. These are stacked to create output .csv

        inputs
        ------
        addresses : list of strings
            Individual addresses in format for API

        call_string : string
            All addresses in API format

    """
    empty_request="https://maps.googleapis.com/maps/api/distancematrix/json?origins={}&destinations={}:&key={}"

    times=np.zeros([len(addresses),len(addresses)])

    for i,ad in enumerate(addresses):
        print("Getting address {}".format(i))
        request=empty_request.format(ad,call_string,key)
        result=requests.get(request).json()

        for j in range(len(addresses)):
            times[i,j]=result["rows"][0]["elements"][j]["duration"]["value"]/60 # extract durations

    np.savetxt(fname,times,fmt="%3.5f", delimiter=",")

if __name__=="__main__":

    file_name="addresses.csv"

    addresses,call_string=get_call_string(file_name)
    call_maps(addresses,call_string,fname="out.csv")