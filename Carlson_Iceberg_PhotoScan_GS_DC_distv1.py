#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creation date: 13 February 2020
Last modified: 11 December 2020
Author: Daniel F. Carlson; daniel.carlson@hzg.de
Affiliation: Helmholtz Zentrum Geesthacht
Collaborators: Urs Treier - Aarhus University
Description: 
    This python script is written for Agisoft PhotoScan Professional v1.4.4 
    Linux Ubuntu computer with 128 GB RAM and a Quadro P1000 CUDA graphics card with 5 compute nodes @1480 MHz, 4006 MB
    Note: PhotoScan has been replaced by MetaShape

    Carlson_Iceberg_PhotoScan_GS_DC_distv1.py performs gradual selection and buils the dense point cloud. During the gradual selection process, 
    thresholds for the reconstruction uncertainty, projection accuracy, and reprojection error are used to identify and remove inaccurate points in the 
    sparse point cloud. This script duplicates the chunk when removing points during each step so the effects of each metric on the sparse point cloud
    can be evaluated. The user provides an initial threshold, which is adjusted through an iterative process that removes as many inaccurate points as
    possible, while still retaining a sufficient number to compute the dense point cloud. The mesh model can also be computed at this point, if desired.
    
    This script was developed using the Agisoft python documentation, forums and from a script by Yu-Hsuan Tu 
    https://github.com/dobedobedo/PhotoScan-Workflow/blob/master/PhotoScan_Workflow.py
    
    For more on Agisoft PhotoScan workflow- see Mayer et al. (2018) A comprehensive workflow to process UAV images for efficient production of accurate
    Geo-information. IX National Conference on Cartography and Geodesy, Lisbon Portugal.
    https://www.researchgate.net/profile/Thomas_Kersten/publication/328841797_A_Comprehensive_Workflow_to_Process_UAV_Images_for_the_Efficient_Production_of_Accurate_Geo-information/links/5be5f929a6fdcc3a8dcb181a/A-Comprehensive-Workflow-to-Process-UAV-Images-for-the-Efficient-Production-of-Accurate-Geo-information.pdf
    
"""
import PhotoScan,  time
import os.path
from datetime import  datetime

# user specified parameters
#
# reconstruction uncertainty threshold
ru_init_threshold = 15
# Dense cloud quality
DenseQual = PhotoScan.HighQuality
# Depth filter mode
DepthFilterMode = PhotoScan.AggressiveFiltering
# Model
# Surface type
SurfType = PhotoScan.SurfaceType.Arbitrary
# Interpolation
ModInterp = PhotoScan.Interpolation.EnabledInterpolation
# FaceCount
ModFaceCount = PhotoScan.FaceCount.HighFaceCount
# Model source data
ModSource = PhotoScan.DataSource.DepthMapsData

def ReduceError_RE(chunk, init_threshold = 0.5):
    # This is used to reduce error based on reprojection error
    #init_threshold = re_init_threshold
    tie_points = chunk.point_cloud
    fltr = PhotoScan.PointCloud.Filter()
    fltr.init(chunk, PhotoScan.PointCloud.Filter.ReprojectionError)
    threshold = init_threshold
    while fltr.max_value > init_threshold :
        fltr.selectPoints(threshold)
        nselected = len([p for p in tie_points.points if p.selected])
        if nselected >= len(tie_points.points) / 10:
            fltr.resetSelection()
            threshold += 0.01
            continue
        tie_points.removeSelectedPoints()
        chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy=True, fit_b1=True, fit_b2=True, 
                              fit_k1=True, fit_k2=True, fit_k3=True, fit_k4=True, 
                              fit_p1=True, fit_p2=True, fit_p3=True, fit_p4=True, 
                              adaptive_fitting=False)
        fltr.init(chunk, PhotoScan.PointCloud.Filter.ReprojectionError)
        threshold = init_threshold

def ReduceError_RU(chunk, ru_init_threshold):
    # This is used to reduce error based on reconstruction uncertainty
    init_threshold = ru_init_threshold
    tie_points = chunk.point_cloud
    fltr = PhotoScan.PointCloud.Filter()
    fltr.init(chunk, PhotoScan.PointCloud.Filter.ReconstructionUncertainty)
    threshold = init_threshold
    while fltr.max_value > ru_init_threshold:
        fltr.selectPoints(threshold)
        nselected = len([p for p in tie_points.points if p.selected])
        if nselected >= len(tie_points.points) / 2 and threshold <= 50:
            fltr.resetSelection()
            threshold += 1
            continue
        tie_points.removeSelectedPoints()
        chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy=True, fit_b1=False, fit_b2=False, 
                              fit_k1=True, fit_k2=True, fit_k3=True, fit_k4=False, 
                              fit_p1=True, fit_p2=True, fit_p3=False, fit_p4=False, 
                              adaptive_fitting=False)
        fltr.init(chunk, PhotoScan.PointCloud.Filter.ReconstructionUncertainty)
        threshold = init_threshold

def ReduceError_PA(chunk, init_threshold=10.0):
    # This is used to reduce error based on projection accuracy
    tie_points = chunk.point_cloud
    fltr = PhotoScan.PointCloud.Filter()
    fltr.init(chunk, PhotoScan.PointCloud.Filter.ProjectionAccuracy)
    threshold = init_threshold
    while fltr.max_value > 10.0:
        fltr.selectPoints(threshold)
        nselected = len([p for p in tie_points.points if p.selected])
        if nselected >= len(tie_points.points) / 2 and threshold <= 12.0:
            fltr.resetSelection()
            threshold += 0.1
            continue
        tie_points.removeSelectedPoints()
        chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy=True, fit_b1=False, fit_b2=False, 
                              fit_k1=True, fit_k2=True, fit_k3=True, fit_k4=False, 
                              fit_p1=True, fit_p2=True, fit_p3=False, fit_p4=False, 
                              adaptive_fitting=False)
        fltr.init(chunk, PhotoScan.PointCloud.Filter.ProjectionAccuracy)
        threshold = init_threshold
    # This is to tighten tie point accuracy value
    chunk.tiepoint_accuracy = 0.1
    chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy=True, fit_b1=True, fit_b2=True, 
                          fit_k1=True, fit_k2=True, fit_k3=True, fit_k4=True, 
                          fit_p1=True, fit_p2=True, fit_p3=True, fit_p4=True, 
                          adaptive_fitting=False)

def BuildDenseCloud(chunk, Quality, FilterMode):
    chunk.buildDepthMaps(quality=Quality,
                             filter=FilterMode,
                             reuse_depth=False)
    chunk.buildDenseCloud(point_colors=True)

def BuildModel(chunk,SurfType,ModInterp, ModFaceCount,ModSource):
    chunk.buildModel(surface=SurfType, 
    interpolation=ModInterp, 
    face_count=ModFaceCount, 
    source=ModSource, 
    vertex_colors=True)
    chunk.buildUV(mapping=PhotoScan.MappingMode.GenericMapping)
    chunk.buildTexture(blending=PhotoScan.MosaicBlending, size = 4096, fill_holes=True,ghosting_filter=True )

# EPSG:4326 Geodetic world coordinate system used by GPS/GNSS sat nav
wgs_84 = PhotoScan.CoordinateSystem("EPSG::4326")

#  list of PhotoScan projects
prj_dir = '/your/project/directory/'
prj_list = ['your', 'list',  'of projects']

time2go = True
tstart = datetime(2020,2,27,18,0,0)

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
        run1oc = doc.chunk
        # gradual selection - 
        # reconstruction uncertainty - Mayer et al. (2018) suggest ru_init_threshold  of 10, here we use 15
        run1gsru = run1oc.copy()
        run1gsru.label = "run1-gs-ru"
        ReduceError_RU(run1gsru, ru_init_threshold)
        # projection accuracy - Mayer et al. (2018) suggest 2-4 for consumer grade cameras
        run1gspa = run1gsru.copy()
        run1gspa.label = "run1-gs-ru-pa"
        ReduceError_PA(run1gspa)
        # reprojection error - Mayer et al. (2018) suggest 0.3 to 0.5
        run1gsre = run1gspa.copy()
        run1gsre.label = "run1-gs-ru-pa-re"
        ReduceError_RE(run1gsre)
        doc.save()
        # build dense cloud
        run1dc =run1gsre.copy()
        run1dc.label = "run1-dc"
        BuildDenseCloud(run1dc,DenseQual, DepthFilterMode)
        doc.save()
        # build mesh and texture
        #BuildModel(run1dc,SurfType,ModInterp, ModFaceCount,ModSource)
        #doc.save()
    else:
        print('invalid directory or file name')
