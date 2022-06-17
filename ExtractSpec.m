clear all
time_count = 0;
spec_count = 0;
cd files/
delete Spec_Data_East_1.nc
mo=['01';'02';'03';'04';'05';'06';'07';'08';'09';'10';'11';'12'];
for location=[1:127]
    for year=[1979:1979]
        
        for m =1:12
            fprintf("year %d month %d  location %d\n", year, m, location)
            if year==1979 && m==1
                
               specdata =  ncread(['location',num2str(location),'_', num2str(year),'_',num2str(m),'.nc'],'SpecData');
               time =  ncread(['location',num2str(location),'_', num2str(year),'_',num2str(m),'.nc'],'Time');
               freq =  ncread(['location',num2str(location),'_', num2str(year),'_',num2str(m),'.nc'],'Freq');
               dep =  ncread(['location',num2str(location),'_', num2str(year),'_',num2str(m),'.nc'],'Dep');
               deg =  ncread(['location',num2str(location),'_', num2str(year),'_',num2str(m),'.nc'],'Deg');
               lat =  ncread(['location',num2str(location),'_', num2str(year),'_',num2str(m),'.nc'],'Lat');
               long =  ncread(['location',num2str(location),'_', num2str(year),'_',num2str(m),'.nc'],'Long');

               nccreate(['Spec_Data_East_',num2str(location),'.nc'],'SpecData','Dimensions',{'x',24,'y',29,'time',netcdf.getConstant('NC_UNLIMITED')} ,'Format', 'netcdf4');
               nccreate(['Spec_Data_East_',num2str(location),'.nc'],'Time','Datatype','string','Dimensions',{"time",netcdf.getConstant('NC_UNLIMITED') })
               nccreate(['Spec_Data_East_',num2str(location),'.nc'],'Freq','Dimensions',{"freq",29})
               nccreate(['Spec_Data_East_',num2str(location),'.nc'],'Dep','Dimensions',{"depth", 1})
               nccreate(['Spec_Data_East_',num2str(location),'.nc'],'Deg','Dimensions',{"degree",24})
               nccreate(['Spec_Data_East_',num2str(location),'.nc'],'Lat','Dimensions',{"lat",1})
               nccreate(['Spec_Data_East_',num2str(location),'.nc'],'Long','Dimensions',{"long",1})
               
               ncwrite(['Spec_Data_East_',num2str(location),'.nc'],'SpecData',specdata);
               ncwrite(['Spec_Data_East_',num2str(location),'.nc'],'Time',time);
               ncwrite(['Spec_Data_East_',num2str(location),'.nc'],'Freq',freq);
               ncwrite(['Spec_Data_East_',num2str(location),'.nc'],'Dep',dep);
               ncwrite(['Spec_Data_East_',num2str(location),'.nc'],'Deg',deg);
               ncwrite(['Spec_Data_East_',num2str(location),'.nc'],'Lat',lat);
               ncwrite(['Spec_Data_East_',num2str(location),'.nc'],'Long',long);
               
               time_count = time_count+length(time);
               spec_count = length(specdata) + spec_count;
               

                continue
            end
               specdata =  ncread(['location',num2str(location),'_', num2str(year),'_',num2str(m),'.nc'],'SpecData');
               time =  ncread(['location',num2str(location),'_', num2str(year),'_',num2str(m),'.nc'],'Time');
         

               ncwrite(['Spec_Data_East_',num2str(location),'.nc'],'SpecData',specdata,[1,1,spec_count]);
               ncwrite(['Spec_Data_East_',num2str(location),'.nc'],'Time',time,time_count);
                
               time_count = time_count+length(time) -1 ;
               spec_count = length(specdata) + spec_count -1;

        
        end
        
    end
end
