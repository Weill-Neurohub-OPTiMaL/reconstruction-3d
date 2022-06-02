# Animation
This documentation details the process of producing 2D and 3D animations based on a folder of json keypoints.

## Convert from json to csv
The animation code takes a csv file, so you must first convert your json files to a csv. You can do this by running `python pose_to_csv.py json_folder save_folder` for 2D keypoints and `python pose_to_csv_3d.py json_folder save_folder` for 3D keypoints.

## Run Animation
To run the animation, run `python animate_pose.py` for 2D keypoints and `python animate_pose_3d.py` for 3D keypoints.