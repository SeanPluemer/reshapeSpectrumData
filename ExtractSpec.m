clear all

mo=['01';'02';'03';'04';'05';'06';'07';'08';'09';'10';'11';'12'];

for year=[1979:1979]
    for m =1:1
            fprintf('Spec2D_',num2str(year),mo(m,:),'.dat.recomp')
            a=fopen(['Spec2D_',num2str(year),mo(m,:),'.dat.recomp'])
            fprintf("Year %d month %d, reading file", year, m)
            b=textscan(a,'%s');
            fclose(a);

        
    end
end
