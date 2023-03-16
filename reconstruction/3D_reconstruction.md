# Reconstruction
This documentation is based off an existing OpenPose tutorial for 2D reconstruction (https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/01_demo.md), but with more detail on the exact commands to run with additional flags as well as instructions for 3D reconstruction.

## 2D Reconstruction
You can use either an image directory or a video. You only need one video because we only need one camera angle for 2D reconstruction.

### Image Method
Get images at a frame rate of 30 frames per second (fps) from a video. I used ffmpeg for this -- see instructions for this in the "ffmpeg" section below. 

Once you have the images from ffmpeg saved in a directory (images must be in the same order as the video), you can run the 2D reconstruction. Here is an example of a command for 2D reconstruction using the image directory `Pictures/wasabi_images`. The keypoint files will be saved under the directory `keypoints/2d_keypoints_1`:
`./build/examples/openpose/openpose.bin --image_dir Pictures/wasabi_images --hand --face --write_json keypoints/2d_keypoints_1 --display 0 --render_pose 0`

### Video Method
Alternatively, you can skip the ffmpeg step and directly input the video into the executable.

Here is an example of a command for 2D reconstruction from a video at the location `Videos/video0_2022-03-11-10-06-04.avi`. The keypoint files will be saved under the directory `keypoints/2d_keypoints_2`:
`./build/examples/openpose/openpose.bin --video Videos/video0_2022-03-11-10-06-04.avi --hand --face --write_json keypoints/2d_keypoints_2 --display 0 --render_pose 0`

## 3D Reconstruction
For 3D reconstruction, I figured out how to do it with an image directory; however, if there is a way to directly input video(s), please let me know.

Make sure your calibration matrices (xml files) are in the directory `openpose/models/cameraParameters/flir`. See `detailed_calibration_documentation.md` located in the `reconstruction` directory for instructions on how to generate calibration matrices. Make sure your calibration matrices are in the correct resolution (HD vs. 4K)! This is very important, otherwise you will get high reconstruction errors with no resulting keypoints (errors are usually in the range of 400-500 pixels when you use the wrong resolution of calibration matrices).

Obtain videos from each of your cameras. Each of these videos has to start at the exact same time. Use the following ffmpeg command to trim the beginnings and ends of your videos so they start at the same point in time:

`ffmpeg -ss 0 -i video0_2022-03-11-10-06-04.avi -vf "trim=start_frame=56:end_frame=356,setpts=PTS-STARTPTS" -c:a copy video_0_trimmed.avi`
* -i specifies the name of the video file
* start_frame and end_frame specify the start and end frames
* -c:a copy specifies the output file name

This command maintains the frame rate and resolution of the video. If you want to use other video editing softwares, such as DaVinci Resolve, make sure that the output video is exporting in the resolution that you are intending (HD vs. 4K).

Your videos and images must be from the same cameras in the same setup that generated your calibration matrices.

Convert to HD using the following ffmpeg command:
`ffmpeg -i /storage/20211117/video0_2021-11-17T20:00:00.011614/video0_2021-11-17-20-00-02.avi -vf scale=1920:1080 -c mjpeg /storage/20211117/video0_2021-11-17T20:00:00.011614_HD/video0_2021-11-17-20-00-02_HD.avi`
* -i specifies the name of the video file you want to convert
* scale=res_width:res_height specifies the HD resolution for width and height.

The videos in Wasabi start out in 4K, but if for some reason you want to convert to 4K if you have a video in a different format, you can simply change `scale=1920:1080` to `scale=4096:2160` in the previous command. Note that conversion to HD takes quite a while (~2 hours for a 1 hour video).

Use ffmpeg to split each of the videos at a frame rate of 30 fps using the following command. For the `cam#` part of the ffmpeg command, make sure to input the camera number of the video you are splitting:

`ffmpeg -i video.avi -vcodec copy cam#_%06d.jpg`
* -i specifies the name of the video file
* The last parameter is the name of the output images. For the above example, if we are using cam0, the images will be named `cam0-000001`, `cam0-000002`, etc. if the "#" is replaced with 0. The 6 is to indicate that there are going to be a number of images in the 6 digits (suitable for 1 hour long videos). If you think you will have a fewer or more number of images based on the length of the videos you're using, change the number accordingly.
* Note that this command will split the video by the frame rate of the input video.

Run the ffmpeg command for splitting videos inside the directory you want the split images to reside in. Split the videos from all three cameras in the same directory. 

Then run the script `RenameInterleave.java` with the command `java RenameInterleave.java <merged_directory>` where merged directory is the single directory with all of your images in the order cam0-000001.png, cam0-000002.png, cam0-000003.png, ... , cam4-000001.png, cam4-000002.png, cam4-000003.png, ... , cam8-000001.png, cam8-000002.png, cam8-000003.png. Running this script will ensure that your images are interleaved in the correct order for the OpenPose 3D reconstruction. Here is some more information about that ordering:
* For each time point, there should be a group of images from that exact same time point for each camera. These groups have to be ordered sequentially in the image directory.
* For example, if I had 2 images each from 3 cameras named as the following: cam0-000001.png, cam0-000002.png, cam4-000001.png, cam4_000002.png, cam8_000001.png, cam8-000002.png, then the order of the images in the image directory that I am doing 3D reconstruction on should be: cam0-000001.png, cam4-000001.png, cam8-000001.png, cam0-000002.png, cam4-000002.png, cam8-000002.png.
* To get these images from each camera, you need a video from each camera recorded at the same time. Make sure the videos are exactly time synced, or you might have high reconstruction error.

Then, you can run the following command:
`./build/examples/openpose/openpose.bin --image_dir ../Pictures/images_for_reconstruction --3d_views 3 --3d --frame_undistort true --number_people_max 1 --hand --face --write_json ../keypoints/3D_keypoints_1 --display 0 --render_pose 0` 
* `../Pictures/images_for_reconstruction` is the interleaved image directory.
* `../keypoints/3D_keypoints_1` is the directory that we want the generated json files containing the 3D keypoints to be located.
* `--3d_views` is the number of cameras.
* `--frame_undistort true` specifies that we are using calibration matrices and we need to perform undistortion before we reconstruct.
* `--hand` and `--face` specify that in addition to body, we want to do reconstruction on the face, right hand, and left hand.
* `--display 0` specifies that we don't want the UI with the video to open up.
* `--render 0` specifies that we don't want the skeletons to be superimposed on the video popup.

On Windows, the executable is in `./build/x64/Release/OpenPoseDemo.exe`, and the rest of the command is the same.

For a 2 minute video, all of these steps take over 14 hours on CPU, but less than 30 minutes total on GPU. 

### Time for each 3D reconstruction step (running on GPU)
1) **Trimming beginning and end of a 2 min video:** 2 min
2) **Downsampling a 2 min video from 4K to HD:** 3 min
3) **Splitting a 2 min video at 30 fps with ffmpeg:** 1 sec
4) **Running RenameInterleave.java on the merged directory (10800 images):** 1 sec
5) **Running 3D reconstruction on the renamed images from step 2:** ~20 mins



## Using ffpmeg
Download ffmpeg here: https://ffmpeg.org/. Detailed instructions for downloading are here: https://www.wikihow.com/Install-FFmpeg-on-Windows. You can run the command following command to get the images:

### Trim the beginning and end of a video
`ffmpeg -ss 0 -i video0_2022-03-11-10-06-04.avi -vf "trim=start_frame=56:end_frame=356,setpts=PTS-STARTPTS" -c:a copy video_0_trimmed.avi`
* -i specifies the name of the video file
* start_frame and end_frame specify the start and end frames
* -c:a copy specifies the output file name

### Convert to HD
`ffmpeg -i /storage/20211117/video0_2021-11-17T20:00:00.011614/video0_2021-11-17-20-00-02.avi -vf scale=1920:1080 -c mjpeg /storage/20211117/video0_2021-11-17T20:00:00.011614_HD/video0_2021-11-17-20-00-02_HD.avi`
* -i specifies the name of the video file you want to convert
* scale=res_width:res_height specifies the HD resolution for width and height.

### Split a video into images
`ffmpeg -i video.avi -vcodec copy cam#_%06d.jpg`
* -i specifies the name of the video file
* The last parameter is the name of the output images. For the above example, if we are using cam0, the images will be named `cam0-000001`, `cam0-000002`, etc. if the "#" is replaced with 0. The 6 is to indicate that there are going to be a number of images in the 6 digits (suitable for 1 hour long videos). If you think you will have a fewer or more number of images based on the length of the videos you're using, change the number accordingly.
* Note that this command will split the video by the frame rate of the input video.

### Find the number of frames in a video
`ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames -of default=nokey=1:noprint_wrappers=1 <video_name>.avi`



## Using scp
To copy files from your local machine to the remote machine, use the following command:
`scp <path to file on your local machine> gsquist@10.0.2.13:~/<path to directory on remote machine>`

`To copy files from remote to local, simply flip the order of the arguments:
`scp gsquist@10.0.2.13:~/<path to directory on remote machine> <path to file on your local machine>`



## Common issues
* Make sure your 3 calibration matrices are located in the correct directory (`openpose\models\cameraParameters\flir`) and they are in the correct resolution (HD vs 4K). HD should be 1920 x 1080, and 4K should be 4096 x 2160 dimensions. 

* Copying video folder contents from Wasabi to Sirius (be in directory name you want the contents to be copied into): `rclone copy secret_sauce:/rcs07/video/20211117/video8_2021-11-17T20:00:00.011615 .` where `.` is the directory `video8_2021-11-17T20:00:00.011615`
Running concat_videos.py: `python3 concat_videos.py /home/gsquist/20211117`



