from netCDF4 import Dataset    # Note: python is case-sensitive!
import numpy as np


ncfile = Dataset('files/new.nc',mode='w',format='NETCDF4_CLASSIC')
ncfile.title='Spec output at specific locations'

long_dim = ncfile.createDimension('long', 273)    # longitude axis
lat_dim  = ncfile.createDimension('lat', 273)
time_dim = ncfile.createDimension('time',273)
freq_dim = ncfile.createDimension('freq', 29)
#depth_dim = ncfile.createDimension('depth', None)
degree_dim = ncfile.createDimension('degree', 36)

data_dim = ncfile.createDimension('data', None)


#location_var = ncfile.createVariable('Location', 'f4', (    'location',))
#y_location_var = ncfile.createVariable('y_loc', 'f4', ('location',))
#time_var = ncfile.createVariable('time', 'f4', ('time',))
#x_data_var = ncfile.createVariable('x', 'f4', ('data',))
#y_data_var = ncfile.createVariable('y', 'f4', ('data',))
#freq_var = ncfile.createVariable('freq', 'f4', ('time',))
#depth_var = ncfile.createVariable('depth', 'f4', ('depth',))
#degree_var = ncfile.createVariable('degree', 'f4', ('degree',))

data_var = ncfile.createVariable("SpecData", 'f4', ("time","long","lat"))
data_var.units = "Unknown"

data_var[0,:,:] = np.random.uniform(0, 100, size=(273, 273))

print(ncfile)


ncfile.close()
ds = Dataset('files/new.nc')
temp = ds.variables["SpecData"][0]
print(temp)
