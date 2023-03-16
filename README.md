# reconstruction-3d
## Author: Nayha Auradkar, nayhaa@cs.washington.edu
Contains calibration, reconstruction, and animation code and documentation for 3D reconstruction in OpenPose. Separated into 1) calibration 2) reconstruction and 3) animation folders. Assumes that you already have the OpenPose repo cloned on your machine and that you are not using flir cameras.

## calibration
If you want to do reconstruction from the patient's home, move the calibration matrices under the `patient_home_calibration_matrices` directory to your openpose repo under the directory `openpose/models/cameraParameters/flir`.

`nayha_home_calibration_matrices` contains calibration matrices from my own home test. For more information on how to create your own calibration matrices, see `detailed_calibration_documentation.md`.

## reconstruction
`3D_reconstruction.md` contains information and commands on how to perform 3D reconstruction from an image directory.

`RenameInterleave` is a supporting file for 3D reconstruction to ensure proper ordering file names of the images to be reconstructed.

## animation
Code for 2D and 3D animations that takes json files of 2D and 3D keypoints as input. See `3D_animation.md` for more information on how to run the animation.

## dev log for this repo
https://github.com/Weill-Neurohub-OPTiMaL/ProjectDocs/wiki/3D-Pose-dev-log
