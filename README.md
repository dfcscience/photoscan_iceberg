# photoscan_iceberg
The photoscan_iceberg repository contains three python scripts for use the Agisoft PhotoScan (https://www.agisoft.com/), which is now MetaShape. These scripts have been used extensively with PhotoScan, and they can be adapted for use with MetaShape, should you so desire. 

Carlson_Iceberg_PhotoScan_Align_distv1.py performs the initial aligment, or bundle adjustment, of your images, and then performs the camera calibration. To use this script, you must first create a project in PhotoScan and name the chunk that you wish to align 'run1'. Then, you must specify the directory and file name(s). You can also change the key point and tie point limits and the accuracy setting. See the comments in the script for more information on how to use this script.

Carlson_Iceberg_PhotoScan_GS_DS_distv1.py performs gradual selection on the sparse point cloud to remove inaccurate points before computing the dense point cloud. Here, you must also specify the directory and file name(s) and you can change thresholds for the reconstruction uncertainty, projection accuracy, reprojection error, and dense cloud quality. The mesh model can also be computed using this script.

Carlson_Iceberg_PhotoScan_DenseCloud_ColorFilter_distv1.py is an optional script that can be used to select points in the dense point cloud by color. It can be useful when cleaning the dense point cloud. 

These scripts were developed to create high resolution 3D mesh models of drifting icebergs in Greenland using UAV images. Links to the UAV imagery and the mesh models are provided below

Iceberg 1, Survey 1, 2017-08-09
https://zenodo.org/record/4306683#.X9MxZFNKjUo

Iceberg 1, Survey 2, 2017-08-11
https://zenodo.org/record/4309826#.X9MxkVNKjUo

Iceberg 1, Survey 3, 2017-08-17
https://zenodo.org/record/4309837#.X9MxpFNKjUo

Iceberg 1, Survey 4, 2017-08-22
https://zenodo.org/record/4309843#.X9MxtVNKjUo

Iceberg 2, Survey 1, 2018-08-20 12:41
https://zenodo.org/record/4309851#.X9MxzlNKjUo

Iceberg 2, Survey 2, 2018-08-20 16:56
https://zenodo.org/record/4309930#.X9Mx41NKjUo

Iceberg 2, Survey 3, 2018-08-21 17:09
https://zenodo.org/record/4309942#.X9Mx9VNKjUo

Iceberg 2, Survey 4, 2018-08-21 21:31
https://zenodo.org/record/4309956#.X9MyClNKjUo

Iceberg 3, Survey 1, 2019-08-03
https://zenodo.org/record/4310136#.X9MyHFNKjUo

Iceberg 3, Survey 2, 2019-08-06
https://zenodo.org/record/4310145#.X9MyMlNKjUo
