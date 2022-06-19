# Calibration Instructions
These instructions are for Windows machines without GPU. You only need 2 cameras for this calibration tutorial, and you can use the built-in camera on your computer as one of the cameras.

## Installing OpenPose
It is possible to complete calibration on a computer with only CPU. Make sure you have a Windows 10 operating system and about 8GB of free RAM.

Follow steps 1 and 2 in the "Windows Prerequisites" section: https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation/1_prerequisites.md#windows-prerequisites . 

Since we will be compiling and running OpenPose, you will want to follow the instructions under the section "Compiling and Running OpenPose from source": https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation/0_index.md#compiling-and-running-openpose-from-source . </br>
**IMPORTANT TIPS:**
* For step 1 (under CMake Configuration), make sure that you add cmake to your PATH environment variable based on where you downloaded the cmake files to -- otherwise, you will not be able to run the cmake command in your terminal. 
* For step 2, there are multiple versions of VS recommended, but I installed the most recent one -- Visual Studio 17 2022. 
* During step 5 of the "Cmake configuration" section, make sure you set the flag WITH_EIGEN to AUTOBUILD (it is set to NONE by default). 

Then, follow this section to compile and run OpenPose: https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation/0_index.md#windows . </br>
**IMPORTANT TIP**:
* Make sure to copy all DLLs from `{build_directory}/bin` into the folder where the generated openpose.dll and *.exe demos are, e.g., `{build_directory}x64/Release` for the 64-bit release version.

## Calibration
OpenPose provides this calibration tutorial: https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/advanced/calibration_module.md#openpose-advanced-doc---calibration-module-and-demo .

I will break down how I did it because the provided calibration tutorial doesn't include how to generate the hundreds of images and record from multiple cameras at a time. It also doesn't have commands with directories that line up with how the openpose repo is structured, so I have included commands that you can simply copy-paste based on how the openpose repo is structured.

### Intrinsic Parameter Calibration
1) Print out this pdf chessboard: https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/advanced/Chessboard_in_PDF/pattern.pdf .
2) Use your computer webcam. Following the "General Quality Tips" here https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/advanced/calibration_module.md#general-quality-tips, take a 20 second video of you holding the chessboard entirely in the camera frame at different distances from the camera frame. 
3) Use ffmpeg to split the images at a frame rate of 30 fps. See the "Using ffmpeg" section below for more details. 
4) In a Linux terminal (I used GitBash), run the following command, making sure that you are the openpose directory:
`./build/x64/Release/Calibration.exe --mode 1 --grid_square_size_mm 30.0 --grid_number_inner_corners "8x6" --camera_serial_number {8-digit_camera_serial_number} --calibration_image_dir {intrinsic_images_folder_path}`.
This will create a directory called `images_with_corners` inside the `{intrinsic_images_folder_path}` directory that has calibration lines on the chessboard. It will also create a file called `{8-digit_camera_serial_number}.xml` in the directory `openpose/models/cameraParameters/flir`.
5) (Optional) To view the undistorted images, run the following command. This will generate another directory inside the `{intrinsic_images_folder_path}` directory called `undistorted_intrinsics`:
`./build/x64/Release/OpenPoseDemo.exe --num_gpu 0 --image_dir {intrinsic_images_folder_path}/images_with_corners --frame_undistort --camera_parameter_path "models/cameraParameters/flir/18079958.xml" --write_images /c/Users/User/CSE600/computer-cam-intrinsic-1/undistorted_intrinsics`
6) Repeat steps 2-5 for your other cameras. 

### Extrinsic Parameter Calibration
1) Record one extrinsic video. Focus on making sure that the chessboard is visible from at least 2 cameras at the time (if you are only using 2 cameras, then the chessboard should be visible from both cameras for the entire video).
* To record from multiple cameras at the same time, use OBS Studio. Download OBS Studio at this link: https://obsproject.com/
* Open OBS Studio. Under the `Sources` window, click the `+` button and then click `Video Capture Device`. Repeat these steps until all of your cameras are added. 
* Under the `Controls` window, click `Start Recording`. 
* Save the video to your machine.
* The video you saved will have multiple videos from different cameras perspectives in the same video. Using https://clideo.com/crop-video, create a separate video for each camera perspectives by cropping out the other cameras' perspectives. Save one video for each camera perspective. 
2) Use ffmpeg to split the images at a frame rate of 30 fps. See the "Using ffmpeg" section below for more details. 
3) Generate the undistorted images. For each camera, run the following command making sure you're in the `openpose/build/x64/Release` directory, creating a different {extrinsic_images_folder_path} for each camera: `./bin/OpenPoseDemo.exe --num_gpu 0 --image_dir /c/Users/User/CSE600/computer-cam-extrinsic-1 --frame_undistort --camera_parameter_path "models/cameraParameters/flir/18079958.xml" --write_images /c/Users/User/CSE600/computer-cam-extrinsic-1/extrinsics`.
4) Consolidate all of the undistorted images from the previous step into one directory `{consolidated_extrinsic_undistorted_images} `. Use the naming convention specified here: https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/advanced/calibration_module.md#naming-convention-for-the-output-images
5) Run the calibration executable between each pair of cameras. There are two flags `--cam0` and `--cam1`. The parameters for these cameras are integers starting from 0 corresponding to an individual camera. 0 is the leftmost camera, 1 is the camera to the right of the 0th camera, and so on. If you have two cameras, here is an example command. You have to be in the outer most `openpose` directory for this or else you won't be able to access your intrinsic xml files: `./build/x64/Release/Calibration.exe --mode 2 --grid_square_size_mm 30.0 --grid_number_inner_corners 8x6 --omit_distortion --calibration_image_dir {consolidated_extrinsic_undistorted_images} --cam0 0 --cam1 1`. This will output your final projection matrix to the terminal. It should be a 3x4 matrix.

## Using ffmpeg
FFmpeg is a free and open source software project that you can use to extract iamges at a certain frame rate from a video.

Download it here: https://ffmpeg.org/. Detailed instructions for downloading are here: https://www.wikihow.com/Install-FFmpeg-on-Windows. You can run the command following command to get the images:

`ffmpeg -i videofile.mov -r 1 image-%04d.png`
* -i specifies the name of the video file
* -r specifies the rate of frames to capture. For example, 1 will save a frame every second, 0.5 will save every 2 seconds, 0.2 every 5 seconds, and 30 every 1/30th of a second.
* The last parameter is the name of the output images. For the above example, the images will be named `image-0001`, `image-0002`, etc.

