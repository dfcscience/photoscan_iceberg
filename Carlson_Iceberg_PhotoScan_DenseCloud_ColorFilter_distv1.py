#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creation date: 11 February 2020
Last Modified: 11 December 2020
Author: Daniel F. Carlson; daniel.carlson@hzg.de
Affiliation: Helmholtz Zentrum Geesthacht

Description: 
    This python script is written for Agisoft PhotoScan Professional v1.4.4 
    Linux Ubuntu computer with 128 GB RAM and a Quadro P1000 CUDA graphics card with 5 compute nodes @1480 MHz, 4006 MB
    Note: PhotoScan has been replaced by MetaShape

    Carlson_Iceberg_PhotoScan_DenseCloud_ColorFilter_distv1.py identifies points in the dense point cloud by color. The user can then inspect the points
    selected by this script and choose to delete them. This script was use to delete dark points on the waterline of icebergs. It may not work if the iceberg
    has a sediment layer.
"""
import PhotoScan
import os.path
prj_dir = '/your/project/directory/'
prj_list = ['your', 'project', 'list']


for p in prj_list:
    fn = prj_dir + p
    if os.path.isfile(fn):
        doc = PhotoScan.app.document
        doc.open(fn)
        run1dccol=doc.chunk
        dense_cloud = run1dccol.dense_cloud
        dense_cloud.selectPointsByColor(color=[0,0,0], tolerance=50, channels='RGB')
        #dense_cloud.removeSelectedPoints()
    else:
        print('invalid directory or file name')
