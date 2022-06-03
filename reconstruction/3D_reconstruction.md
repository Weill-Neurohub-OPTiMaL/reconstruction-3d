# Reconstruction
This documentation is based off this existing OpenPose tutorial for 2D reconstruction, but with more detail on the exact commands to run with additional flags as well as instructions for 3D reconstruction: https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/01_demo.md

## 2D Reconstruction
You can use either an image directory or a video. You only need one video because for 2D, we only need one camera angle.

### Image Method
Get images at a frame rate of 30 frames per second (fps) from a video. I used ffmpeg for this -- see instructions for this in the "ffmpeg" section below. 

Once you have the images from ffmpeg saved in a directory, you can run the 2D reconstruction. Here is an example of a command for 2D reconstruction from the image directory `/c/Users/User/openpose/examples/media/wasabi_images/`:
`./build/x64/Release/OpenPoseDemo.exe --image_dir /c/Users/User/openpose/examples/media/wasabi_images/ --hand --face --write_json /c/Users/User/CSE600/openpose/2d_keypoints_1 --display 0 --render_pose 0`

### Video Method
Alternatively, you can skip the ffmpeg step and directly input the video into the executable. I think the video has to be in .avi format, but let me know if find otherwise.

Here is an example of a command for 2D reconstruction from a video at the location `/c/Users/User/openpose/examples/media/wasabi_images/`:
`./build/x64/Release/OpenPoseDemo.exe --video /c/Users/User/openpose/examples/media/video0_2022-03-11-10-06-04.avi --hand --face --write_json /c/Users/User/CSE600/openpose/2d_keypoints_1_from_video --display 0 --render_pose 0`

## 3D Reconstruction
For 3D reconstruction, I only figured out how to do it with an image directory; however, if there is a way to directly input video(s), please let me know.

Make sure your calibration matrices (xml files) are in the directory `openpose/models/cameraParameters/flir`. See `detailed_calibration_documentation.md` for instructions on how to generate calibration matrices.

Obtain videos from each of your cameras. Each of these videos has to start at the exact same time. Your videos/images must be from the same cameras in the same setup that generated your calibration matrices. 

Use ffmpeg to split each of the videos at a frame rate of 30 fps. See the "ffmpeg" section below for more detailed instructions. I would recommend creating 3 different directories (one for each camera) with each directory containing the images in the same order of the video progression. For 3 cameras, rename the images in the camera 0 directory as "cam0 (1)", "cam0 (2)", "cam0 (3)", etc. Then, rename the images in the camera 4 directory as "cam4 (1)", "cam4 (2)", "cam4 (3)", etc. and the images in the camera 8 directory as "cam8 (1)", "cam8 (2)", "cam8 (3)", etc. Windows file explorer allows you to batch rename with the following steps:
1) Select (highlight) all the files you want to rename.
2) Right-click the first of the highlighted files and click “Rename.”
3) Type in the new file name and press the Enter key. All selected files will be renamed, using a “<file name> (number)” format to keep each file individually identifiable. For example, if you typed in "cam 0" as the file name, the files would be renamed as "cam0 (1)", "cam0 (2)", "cam0 (3)", etc.

After you have renamed the files in the three directories, merge the directories into a single directory, where the images are in the order "cam0 (1)", "cam0 (2)", "cam0 (3)", ... , cam4 (1), cam 4(2), cam4(3), ... , cam8(1), cam8(2), cam8(3)".

Then run the script `RenameInterleave.java` with the command `java RenameInterleave.java <merged_directory>` where merged directory is the single directory with all of your images. This will ensure that your images are interleaved in the correct order for the OpenPose 3D reconstruction. Here's more information about that ordering if you're interested: 
* For each time point, there should be a group of images from that exact same time point for each camera. These groups have to be ordered sequentially in the image directory.
* For example, if I had 2 images each from 3 cameras named as the following: cam0 (1), cam0 (2), cam4 (1), cam4 (2), cam8 (1), cam8 (2), then the order of the images in the image directory that I am doing 3D reconstruction on should be: cam0 (1), cam4 (1), cam8 (1), cam0 (2), cam4 (2), cam8 (2)
* To get these images from each camera, you need a video from each camera recorded at the same time. Make sure the videos are exactly time synced, or you might run into reconstruction error. You can use ffmpeg as described above to get frames at the rate that you desire.

Then, you can run the following command where 
* `/c/Users/User/openpose/examples/media/images_for_reconstruction/` is the interleaved image directory.
* `/c/Users/User/openpose/json_keypoints` is the directory that we want the generated json files containing the 3D keypoints to be located.
* `--3d_views` is the number of cameras.
* `--frame_undistort true` specifies that we are using calibration matrices and we need to perform undistortion before we construct.
* `--hand` and `--face` specify that in addition to body, we want to do reconstruction on the face, right hand, and left hand.
* `--display 0` specifies that we don't want the UI with the video to open up.
* `--render 0` specifies that we don't want the skeletons to be superimposed on the video popup.

Here is the full command:
`./build/x64/Release/OpenPoseDemo.exe --image_dir /c/Users/User/openpose/examples/media/images_for_reconstruction/ --3d_views 3 --3d --frame_undistort true --number_people_max 1 --hand --face --write_json /c/Users/User/openpose/json_keypoints --display 0 --render_pose 0`

All of these steps take over 12 hours on CPU, but only about 10 minutes on GPU. 

## Using ffpmeg
Download ffmpeg here: https://ffmpeg.org/. Detailed instructions for downloading are here: https://www.wikihow.com/Install-FFmpeg-on-Windows. You can run the command following command to get the images:

`ffmpeg -i videofile.mov -r 30 image-%04d.png`
* -i specifies the name of the video file
* -r specifies the rate of frames to capture. For example, 1 will save a frame every second, 0.5 will save every 2 seconds, 0.2 every 5 seconds, and 30 every 1/30th of a second.
* The last parameter is the name of the output images. For the above example, the images will be named `image-0001`, `image-0002`, etc.

## Using scp
To copy files from your local machine to the remote machine, use the following command:
`scp <path to file on your local machine> gsquist@10.0.2.13:~/<path to directory on remote machine>`

`To copy files from remote to local, simply flip the order of the arguments:
`scp gsquist@10.0.2.13:~/<path to directory on remote machine> <path to file on your local machine>`





