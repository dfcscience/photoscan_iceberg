#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creation date: 11 February 2020
Last Modified: 11 December 2020
Author: Daniel F. Carlson; daniel.carlson@hzg.de
Affiliation: Helmholtz Zentrum Geesthacht
Collaborator:  Urs Treier, Aarhus University

Description: 
    This python script is written for Agisoft PhotoScan Professional v1.4.4 
    Linux Ubuntu computer with 128 GB RAM and a Quadro P1000 CUDA graphics card with 5 compute nodes @1480 MHz, 4006 MB
    Note: PhotoScan has been replaced by MetaShape

    Carlson_Iceberg_PhotoScan_Align_distv1.py performs the initial alignment of aerial drone imagery in PhotoScan and will loop through a user-specified list of project file names. 
    Other user-specified parameters include the image quality filter, accuracy, preselections, key point limit and tie point limit
    
    This script was developed using the Agisoft python documentation, forums and from a script by Yu-Hsuan Tu 
    https://github.com/dobedobedo/PhotoScan-Workflow/blob/master/PhotoScan_Workflow.py
    
    NOTE: When creating your projects, add a chunk, and then rename it 'run1'
    
    After executing this script, check the initial alignment of each project and the bounding box.
    
    Resize the bounding box, if necessary and then run to perform gradual selection, ... 
    
"""
import PhotoScan,  time
import os.path
from datetime import  datetime

# User-Specified Parameters
#
# Image Quality - PhotoScan can estimate image quality by analyzing the contrast between pixels. The algorithm assumes that high contrast = sharp image and low contrast = blurred image
# A number that is usually between 0 and 1, but can be higher than 1.
# The quality estimate is not reliable so we set 'CheckQuality' to False by default.
CheckQuality = False
QualityThresh = 0.5

# Alignment Accuracy
# Options: HighestAccuracy, HighAccuracy, MediumAccuracy, LowAccuracy, LowestAccuracy
AlignAccuracy = PhotoScan.Accuracy.HighAccuracy

# Key Point Limit
# The key point limit sets the number of features considered in each photo. The default settings work for a computer with less RAM but here we have 64 GB so we increase it to 60000
KeyLim = 60000

# Tie Point Limit
# The tie point limit sets the maximum number of features that are recognizable, and matched, in multiple photos. Setting it to zero removes the limit
TieLim = 0

# Generic Preselection
# Generic preselection uses lower resolution copies of the original images to attempt to find overlap. Disabling generic preselection compares each image to every other image and can increase processing time
GenPre = False

# Reference Preselection
# Reference preselection uses camera position data (and orientation, if available) to preselect images based on the location of each image. We are aligning drone imagery with position data embedded in the exif metadata of each image 
RefPre = False

# Optimize Cameras
# Fit lens parameters
OptCam = True
ff =True 
fcx=True 
fcy=True 
fb1=False 
fb2=False 
fk1=True 
fk2=True 
fk3=True 
fk4=False 
fp1=True 
fp2=True
fp3=False
fp4=False 
adaptfit=False

# GPS location accuracy in meters
SetGPSaccuracy = False
gps_acc_hor = 20
gps_acc_ver = 5

def ImQuality(QualityThresh, chunk):
    if chunk.cameras[0].meta['Image/Quality'] is None:
        chunk.estimateImageQuality()
        for band in [band for camera in chunk.cameras for band in camera.planes]:
            if float(band.meta['Image/Quality']) < QualityThresh:
                band.enabled = False

def AlignChunk(chunk, AlignAccuracy,KeyLim ,TieLim ,GenPre,RefPre):
    chunk.matchPhotos(accuracy = AlignAccuracy, 
    generic_preselection = GenPre,
    reference_preselection=RefPre,
    filter_mask=True,
    keypoint_limit=KeyLim,
    tiepoint_limit=TieLim)
    realign_list = list()
    for camera in chunk.cameras:
        if not camera.transform:
            realign_list.append(camera)
    if len(realign_list) > 0:
        chunk.alignCameras(cameras = realign_list)

def OptimizeCameras(chunk,ff,fcx,fcy,fb1,fb2,fk1,fk2,fk3,fk4,fp1,fp2,fp3,fp4,adaptfit):
    chunk.optimizeCameras(fit_f=ff, fit_cx=fcx, fit_cy=fcy, fit_b1=fb1, fit_b2=fb2, 
                          fit_k1=fk1, fit_k2=fk2, fit_k3=fk3, fit_k4=fk4, 
                          fit_p1=fp1, fit_p2=fp2, fit_p3=fp3, fit_p4=fp4, 
                          adaptive_fitting=adaptfit)

# EPSG:4326 Geodetic world coordinate system used by GPS/GNSS sat nav
wgs_84 = PhotoScan.CoordinateSystem("EPSG::4326")

#  list of PhotoScan projects
prj_dir = '/your/project/directory/'
prj_list = ['your', 'project', 'list']

# wait to start until your officemate leaves for the day so they don't have to listen to the cooling fan
time2go = True
tstart = datetime(2020,2,12,16,53,0)

while not time2go:
    time.sleep(30)
    tdif = datetime.now() - tstart
    seconds = tdif.total_seconds()
    if seconds > 0:
        time2go = True

# project loop
for p in prj_list:
    fn = prj_dir + p
    if os.path.isfile(fn):
        doc = PhotoScan.app.document
        doc.open(fn)
        run1 = doc.chunk
        # set GPS accuracy
        if SetGPSaccuracy:
            run1.camera_location_accuracy = PhotoScan.Vector([gps_acc_hor, gps_acc_hor,gps_acc_ver])
        # check to see if images are already aligned
        if run1.point_cloud is None:
            if CheckQuality:
                ImQuality(QualityThresh, run1)
            AlignChunk(run1, AlignAccuracy, KeyLim,  TieLim,  GenPre,  RefPre)
            if OptCam:
                run1oc = run1.copy()
                run1oc.label = "run1-oc"
                OptimizeCameras(run1oc,ff,fcx,fcy,fb1,fb2,fk1,fk2,fk3,fk4,fp1,fp2,fp3,fp4,adaptfit)
            doc.save()
        else:
            print('Already Aligned')
    else:
        print('file does not exist')
