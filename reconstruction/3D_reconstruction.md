# Reconstruction
2D reconstruction is relatively straightforward, so this documentation focuses mainly on 3D reconstruction. This documentation is based off this existing OpenPose tutorial, but with more detail on the exact commands to run with additional flags: https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/01_demo.md

## 2D Reconstruction
You can use either an image directory or a video. I did my reconstruction by getting images at a certain frame rate from a video and then running reconstruction on that image directory. Here is an example of a command for 2D reconstruction from the image directory `/c/Users/User/openpose/examples/media/wasabi_images/`:
`./build/x64/Release/OpenPoseDemo.exe --image_dir /c/Users/User/openpose/examples/media/wasabi_images/ --hand --face --write_json /c/Users/User/CSE600/openpose/2d_keypoints_1 --display 0 --render_pose 0`

## 3D Reconstruction
For 3D reconstruction, the images have to be in a specific order and from specific cameras. 
* Make sure your calibration matrices (xml files) are in the directory `openpose/models/cameraParameters/flir`. 
* Your images must be from the same cameras in the same setup that generated your calibration matrices. 
* For each time point, there should be a group of images from that exact same time point for each camera. These groups have to be ordered sequentially in the image directory.
* For example, if I had 2 images each from 3 cameras named as the following: img_1_cam_0, img_2_cam_0, img_1_cam_4, img_2_cam_4, img_1_cam_8, img_2_cam_8, then the order of the images in the image directory that I am doing 3D reconstruction on should be: img_1_cam_0, img_1_cam_4, img_1_cam_8, img_2_cam_0, img_2_cam_4, img_2_cam_8

Then, you can run the following command where `/c/Users/User/openpose/examples/media/images_for_reconstruction/` is the directory where the images that we want to do 3D reconstruction on are located and `/c/Users/User/openpose/json_keypoints` is the directory that we want the generated json files containing the 2D and 3D keypoints to be located. `--3d_views` is 3 here because we have 3 cameras. `--frame_undistort true` specifies that we are using calibration matrices and we need to perform undistortion before we construct. `--hand` and `--face` specify that in addition to body, we want to do reconstruction on the face, right hand, and left hand. `--display 0` and `render 0` specify that we don't want to open up the OpenPose UI and see the skeletons, we just want to generate the json files.
`./build/x64/Release/OpenPoseDemo.exe --image_dir /c/Users/User/openpose/examples/media/images_for_reconstruction/ --3d_views 3 --3d --frame_undistort true --number_people_max 1 --hand --face --write_json /c/Users/User/openpose/json_keypoints --display 0 --render_pose 0`



