spec_file_name = "Spec2D_"
from netCDF4 import Dataset

def main():
    locations = generate_locations("Spec2D_197901.dat.recomp")
    number_points = len(locations)
    first_run(number_points)
    save_inital_var(locations)
    full_spec_data = []
    full_time_data = []
    for year in range(1979,1980 ):
        for month in range(1,13):
            print("working on: ", year, month)
            month_use = str("{:02d}".format(month))
            file_data = readinfiledata(spec_file_name + str(year) + month_use + ".dat.recomp")
            tempdata, temptime = extract_data(locations,file_data)
            full_spec_data.append(tempdata)
            full_time_data.append(temptime)
        full_time_data,full_spec_data =  remove_duplicates(full_spec_data,locations,full_time_data)
        save_nc_fast(full_spec_data,locations, full_time_data)
        #the structure of the full_spec_data is
        #[month][location][y][x]



def save_inital_var(location):
    locations=[]
    for i in range(len(location)):
        locations.append(location[i].split())
    freq = []
    dir = []
    dep = []
    with open("freq.txt") as f:
        for line in f:
            freq.append(float(line))
    with open("dir.txt") as f:
        for line in f:
            dir.append(float(line))
    with open("dep.txt") as f:
        for line in f:
            dep.append(float(line))

    for i in range(len(location)):
        locations.append(location[i].split())
        infile = Dataset("files/location" + str(i) + ".nc", "a")
        infile['Long'][:] = locations[i][0]
        infile['Lat'][:] = locations[i][1]
        infile['Freq'][:] = freq
        infile['Deg'][:] = dir
        infile['Dep'][:] = dep[i]
        infile.close()

def extract_data(locations, data):
    time = 0
    total_time = sum('date' in s for s in data)
    spec_data = [[[]for _ in range(total_time)] for _ in range(len(locations)) ]
    time_list = []
    for i in range(len(data)):
        temp = []
        if ("date and time" in data[i]):
            time_list.append(data[i])
            time +=1
            location_number = 0

            #this means that I am at the start of a new time.
        if ("FACTOR" in data[i]):
            #this means that I am at a new location
            factor_number = float(data[i+1])
            test = i + 2

            while "FACTOR" not in data[test] and "date" not in data[test] and test < len(data):
                tester = list(data[test].split())
                my_new_list = [float(j) * factor_number for j in tester]
                spec_data[location_number][time-1].append(my_new_list)
               # temp.append(my_new_list)
                test +=1
                if (test == len(data)):
                    break

            location_number +=1
    hello = []
    for i in range(len(time_list)):
        hello.append(time_list[i].split()[0])
    #spec_data is the list of data at the specific locations, East = list(127/x,y)
    #locations is the list of locations, east (127)
    #total time is the count of how many hours in that month
    #hello is the actual list of times
    return spec_data, hello

    #so i am thinking it might be worth getting the entire run and then saving it?
def flatten(xss):
    return [x for xs in xss for x in xs]

def remove_duplicates(data,locations,time_list):
    for month in range(1,len(time_list)):
        for location in range(len(locations)):
            del data[month][location][:len(locations)] #note, when this is used it deletes the orig data from main
        time_list[month].pop(0)
    return time_list, data
def save_nc_fast(data,locations, time_list):

    import numpy as np
    flat_list = []
    for xs in time_list:
        for x in xs:
            flat_list.append(x)
    times = np.array(flat_list, dtype=object)
    j = 0

    for i in range(len(locations)):
        infile = Dataset("files/location" + str(i) + ".nc", "a")
        infile['Time'][:] = times
        time = 0
        for month in range(len(time_list)):
            for idk in range(len(data[month][i])):
                    infile['SpecData'][:,:,time] = data[month][i][idk]
                    time+=1
                    print(i, month, time, idk)

        print( i,month, time, idk)
        infile.close()


def first_run(number_locations):
    for i in range(number_locations+1):
        ncfile = Dataset('files/location' + str(i) + ".nc", mode='w')
        ncfile.title = 'Spec output at specific locations'

        long_dim = ncfile.createDimension('long', 1)  # longitude axis
        lat_dim = ncfile.createDimension('lat', 1)
        time_dim = ncfile.createDimension('time', None)
        depth_dim = ncfile.createDimension('depth', 1)
        freq_dim = ncfile.createDimension('freq', 29)
        degree_dim = ncfile.createDimension('degree', 24) #29 for gom
        x_dim = ncfile.createDimension("x", 24)  # 36 for gom

        y_dim = ncfile.createDimension("y", 29)  # this is setting the expected number of "data points" per month
        spec_var = ncfile.createVariable("SpecData", 'f4', ("x", "y", "time"))

        Long_var = ncfile.createVariable("Long", 'f4', ("long"))
        Lat_var = ncfile.createVariable("Lat", 'f4', ("lat"))
        Freq_var = ncfile.createVariable("Freq", 'f4', ("freq"))
        Deg_var = ncfile.createVariable("Deg", 'f4', ("degree"))
        Dep_var = ncfile.createVariable("Dep", 'f4', ("depth"))
        Time_var = ncfile.createVariable('Time', str, "time",)
        ncfile.close()

def readinfiledata(file):
    temp = []
    start = False
    with open(file) as f:
        for line in f:
            if("date and time" in line):
                start = True
            if (start):
                temp.append(line)
    return temp

def generate_locations(file):
    temp = []
    start = False
    with open(file) as f:
        for line in f:
            if ("AFREQ" in line):
                return temp
            if (start):
                temp.append(line)
            if("number of locations" in line):
                start = True

if __name__ == '__main__':
    import cProfile
    cProfile.run("main()", "output.dat")

    import pstats
    from pstats import SortKey
    with open("output_time.txt", "w") as f:
        p = pstats.Stats("output.dat", stream=f)
        p.sort_stats("time").print_stats()

    with open("output_calls.txt", "w") as f:
        p = pstats.Stats("output.dat", stream=f)
        p.sort_stats("calls").print_stats()
