spec_file_name = "Spec2D_"
from netCDF4 import Dataset

def main():
    locations = generate_locations("Spec2D_202001.dat")
    number_points = len(locations)
    first_run(number_points)
    save_inital_var(locations)
    for year in range(2020,2021 ):
        for month in range(1,2):
            print("working on: ", year, month)
            month_use = str("{:02d}".format(month))
            file_data = readinfiledata(spec_file_name + str(year) + month_use + ".dat")
            extract_data(locations,file_data)


def save_inital_var(location):
    locations=[]
    for i in range(len(location)):
        locations.append(location[i].split())
    freq = []
    dir = []
   # dep = []
    with open("freq.txt") as f:
        for line in f:
            freq.append(float(line))
    with open("dir.txt") as f:
        for line in f:
            dir.append(float(line))
  #  with open("dep.txt") as f:
  #      for line in f:
  #          dep.append(float(line))
    for i in range(len(location)):
        locations.append(location[i].split())
        infile = Dataset("files/location" + str(i) + ".nc", "a")
        infile['Long'][:] = locations[i][0]
        infile['Lat'][:] = locations[i][1]
    infile['Freq'][:] = freq
    infile['Deg'][:] = dir
    #infile['Dep'][:] = dep
    infile.close()

def extract_data(locations, data):
    time = 0
    total_time = sum('date' in s for s in data)
    spec_data = [[[]for _ in range(total_time)] for _ in range(len(locations)) ]

    for i in range(len(data)):
        temp = []
        if ("date and time" in data[i]):
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

           # save_data(temp,locations[location_number])
            #save_nc(temp,location_number,time-1)
            location_number +=1
            #i = test

    save_nc_fast(spec_data,locations,total_time)

def save_nc(data,location,time):

    infile= Dataset("files/location" + str(location) + ".nc" , "a")
    infile['SpecData'][:,:,time] = data
    infile.close()

def save_nc_fast(data,locations, timex):
    print("saving")
    for i in range(len(locations)):
        infile = Dataset("files/location" + str(i) + ".nc", "a")
        for j in range(time):
            infile['SpecData'][:,:,j] = data[i][j]
        infile.close()


def first_run(number_locations):
    for i in range(number_locations+1):
        ncfile = Dataset('files/location' + str(i) + ".nc", mode='w', format='NETCDF4_CLASSIC')
        ncfile.title = 'Spec output at specific locations'

        long_dim = ncfile.createDimension('long', 1)  # longitude axis
        lat_dim = ncfile.createDimension('lat', 1)
        x_dim = ncfile.createDimension("x", 36)
        y_dim = ncfile.createDimension("y", 29)
        time_dim = ncfile.createDimension('time', None)
        depth_dim = ncfile.createDimension('depth', 1)
        freq_dim = ncfile.createDimension('freq', 29)
        degree_dim = ncfile.createDimension('degree', 36)

        spec_var = ncfile.createVariable("SpecData", 'f4', ("x", "y", "time"))
        Long_var = ncfile.createVariable("Long", 'f4', ("long"))
        Lat_var = ncfile.createVariable("Lat", 'f4', ("lat"))
        Freq_var = ncfile.createVariable("Freq", 'f4', ("freq"))
        Deg_var = ncfile.createVariable("Deg", 'f4', ("degree"))
        Dep_var = ncfile.createVariable("Dep", 'f4', ("depth"))
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
    with open("output_time_old.txt", "w") as f:
        p = pstats.Stats("output.dat", stream=f)
        p.sort_stats("time").print_stats()

    with open("output_calls_old.txt", "w") as f:
        p = pstats.Stats("output.dat", stream=f)
        p.sort_stats("calls").print_stats()


#todo list
#First, I need to open the Spec file and count how many locations there are
#second, I need to see if the freq, and degrees are the same for each year, they should be.
#third, make a csv file with the freq, degree, dep
#fourth, I need to open the dat file
'''1.	How to open the data
a.	Open file
b.	Go to next timeslot
i.	Read in the factor
ii.	Read in chart
iii.	Multiply chart by factor
iv.	 Store the data in the 3d array 
c.	When at the end of the file, time to save the nc file.
d.	
'''