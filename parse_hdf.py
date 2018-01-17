#!/usr/bin/python
# coding:utf-8


from pyhdf.SD import SD
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, shiftgrid
import numpy as np
import os


def parse_hdf(filename):
    hdf_file = '{path}/data/{filename}'.format(
        path=sys.path[0],
        filename=filename
    )
    file = SD(hdf_file)
    print log_string, 'file info: ', file.info()
    datasets_dict = file.datasets()
    print log_string, '数据集：'
    for idx, sds in enumerate(datasets_dict):
        sds_obj = file.select(sds)
        data = sds_obj.get()
        data_attr = sds_obj.attributes()
        availabe_dict[sds] = data
        print log_string, idx, sds, ' :', data.shape
    file.end()


def draw_all():
    title = 'Wind_Speed_Ncep_Ocean'
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    b_map = Basemap(resolution='l', area_thresh=10000, projection='cyl', llcrnrlon=73, urcrnrlon=135,
                    llcrnrlat=3,
                    urcrnrlat=53)
    b_map.drawcoastlines(linewidth=0.8)

    for root, dirs, files in os.walk(sys.path[0]+"/data/"):
        for file in files:
            parse_hdf(file)
            lon = availabe_dict['Longitude']
            lat = availabe_dict['Latitude']
            target = availabe_dict[title]
            x, y = b_map(lon, lat)
            #lon, lat = shiftgrid(180, lon, lat)
            #x, y = b_map(lon, lat)
            cs = b_map.contourf(x, y, target)
            b_map.colorbar(cs)
    plt.title('Deep_Blue_Aerosol_Optloical_Depth_550_Land_STD', size=20)
    plt.show()


log_string = 'log  '
availabe_dict = {}
draw_all()
