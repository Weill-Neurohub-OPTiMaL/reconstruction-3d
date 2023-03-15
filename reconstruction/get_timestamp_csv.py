import json, pdb, datetime, os, fnmatch, hashlib, re, csv, cv2
import pandas as pd
import numpy as np
# from raw_vid_utils import *
from datetime import timedelta
import json, subprocess, datetime, re
import os.path
from pathlib import Path
import subprocess

import numpy as np
import pandas as pd


# def get_timestamp_csv(video_path, json_path, save_path):
#     meta_file = json.load(open(json_path))
#     real_record_start_time = meta_file['recordStartTime']
#     real_record_end_time = meta_file['recordEndTime']
#     fps = int(meta_file['frame_rate'])
#     recording_duration = int(meta_file['recording_sesh_len']) #in seconds
#     num_frames = recording_duration*fps
#     num_intervals = num_frames - 1

#     #calculate estimated times per frame
#     estimate_cfr_timestamp = est_cfr_timestamps(num_frames, fps)
#     full_end_datetime = datetime.datetime.strptime(real_record_end_time.split("T")[0] + ' ' + real_record_end_time.split("T")[1], "%Y-%m-%d %H:%M:%S.%f")
#     estimate_cfr_datetimestamp = [0]*len(estimate_cfr_timestamp)
#     #Use estimated cfr times to decrement back from recordEndTime
#     for i in range(len(estimate_cfr_timestamp)):
#         estimate_cfr_datetimestamp[i] = decrement_by_framenum(full_end_datetime, estimate_cfr_timestamp[i])
#     estimate_cfr_datetimestamp.reverse()
#     print("estimate_cfr_datetimestamp type: ", type(estimate_cfr_datetimestamp))
#     print("estimate_cfr_datetimestamp len: ", len(estimate_cfr_datetimestamp))
#     # np.save(granger_lp+"estimate_cfr_times_" + recording_name + ".npy", estimate_cfr_datetimestamp)

#     # Calculate range of time covered by calculated times, compare to expected range
#     beginning = datetime.datetime.strptime(estimate_cfr_datetimestamp[0].split("T")[0] + ' ' + estimate_cfr_datetimestamp[0].split("T")[1], "%Y-%m-%d %H:%M:%S.%f")
#     end = datetime.datetime.strptime(estimate_cfr_datetimestamp[-1].split("T")[0] + ' ' + estimate_cfr_datetimestamp[-1].split("T")[1], "%Y-%m-%d %H:%M:%S.%f")
#     print("Time range covered by calculated cfr-times:",end - beginning)
#     expected_range = (num_intervals / fps)
#     print("Expected range:", timedelta(seconds=round((num_intervals / fps), 6)))

#     with open(save_path, "w", newline="") as f:
#         # Create a CSV writer
#         writer = csv.writer(f)
#         # Write the list of strings to the CSV file, one row at a time
#         for string in estimate_cfr_datetimestamp:
#             writer.writerow([string])


def all_here(directory, **kwargs):
    """
    returns all files in given directory
    Optionally sub-select files within a given time range
    Parameters
    ----------
    directory: string, directory path
    kwargs:
        start_time: string, should be a pandas datetime object, localized to US/Pacific
        end_time: string, should be a pandas datetime object, localized to US/Pacific
        timestamps: list, should contain pandas datetime objects localized to US/Pacific
    """
    all_files = [f for f in os.listdir(directory) if not f.startswith('.')]

    if kwargs.get('timestamps'):
        selection = np.array([True] * len(all_files))
        timestamps = np.array(kwargs.get('timestamps'))
        if kwargs.get('start_time'):
            selection = np.logical_and(selection, timestamps >= kwargs.get('start_time'))
        if kwargs.get('end_time'):
            selection = np.logical_and(selection, timestamps < kwargs.get('end_time'))
        return np.array(all_files)[selection]

    return all_files


def estimate_constant_frame_rate_timestamps(total_num_frames, fps):
    """
    Returns millisecond-precision times
    for every frame in a video based on
    a constant frame rate (cfr) assumption
    help from https://stackoverflow.com/questions/47743246/getting-timestamp-of-each-frame-in-a-video
    :param total_num_frames: The number of frames we want timestamps for
    :param fps: the frame rate which videos were recorded at
    """
    cfr_times = []
    for i in range(int(total_num_frames)):
        cfr_times.append(
            round((float(i) / fps) * 1000, 6))  # How opencv/ffmpeg handles this: 1000.0*(double)frame_number/get_fps();
    return cfr_times


def decrement_by_frame_num(date_string, decrement):
    """
    Returns datetimestamp format after decrementing by milliseconds
    that are calculated by frame number i.e. 1000.0*(frame_number/fps)
    :param date_string: datetime to be decremented
    :param decrement: the number of milliseconds to subtract from date_string
    """
    fulldate = str(date_string - datetime.timedelta(milliseconds=decrement))
    return fulldate.split()[0] + "T" + fulldate.split()[1]


def adjust_constant_frame_rate_timestamps(recording_end_datetime, num_frames, fps):
    """
    writes out millisecond-level-precision timestamps for videos
    recorded at a constant frame rate (cfr).
    The timestamps are first estimated in estimate_constant_frame_rate_timestamps(),
    then adjusted by the recording_end_datetime timestamp, which is most-precise
    end-of-recording time that we have for videos captured with a cfr in the CameraApp v0.
    :param recording_end_datetime: type string; value comes from video metadata files generated
    immediately after the end of a video recording
    :param num_frames: duration of video we're generating timestamps for
    :param fps: frame rate videos were captured at
    returns timestamps as pandas dataframe
    """

    estimate_cfr_timestamp = estimate_constant_frame_rate_timestamps(num_frames, fps)
    estimate_cfr_datetimestamp = [0] * len(estimate_cfr_timestamp)
    for i in range(len(estimate_cfr_timestamp)):
        estimate_cfr_datetimestamp[i] = decrement_by_frame_num(pd.to_datetime(recording_end_datetime),
                                                               estimate_cfr_timestamp[i])
    estimate_cfr_datetimestamp.reverse()
    return pd.DataFrame({'timestamp': estimate_cfr_datetimestamp})


def get_video_end_time(video_path):
    """
   Get recording end from video metadata file
   :param video_path: should match /wasabi_mount_location/patientID/video/date/video#_datetime/
   returns timestamp as type string
   """
    for file in os.listdir(os.path.join(video_path)):
        if file.startswith("metadata_"):
            with open(video_path + "/" + file) as meta_data_file:
                metadata = json.load(meta_data_file)
                return metadata["recordEndTime"]


def get_recording_segment_len(video_path):
    """
   Get recording_segment_len from video metadata file
   :param video_path: should match /wasabi_mount_location/patientID/video/date/video#_datetime/
   returns timestamp as type string
   """
    for file in os.listdir(os.path.join(video_path)):
        if file.startswith("metadata_"):
            with open(video_path + "/" + file) as meta_data_file:
                metadata = json.load(meta_data_file)
                return metadata["recording_segment_len"]


def get_start_indices_close_to_latest_camera(video_path, fps):
    """
    For now 3D pose should have sequence of images input
    with exact-as-possible start times to improve
    accuracy. Cameras start slightly off from each other,
    so this returns the approximate index (corresponding to the frame)
    of when cameras that started earlier match the start time
    of the latest camera
    :param video_path: should be /wasabi_mount_location/patientID/video/date/
    :param fps: frame rate video was captured at (assumes constant frame rate for now)
    """
    video_directories = all_here(video_path)
    video_dfs = pd.DataFrame()
    for camera_dir in video_directories:
        recording_duration = get_recording_segment_len(video_path + camera_dir)  # in seconds
        # print("recording_duration: ", type(recording_duration))
        # print("fps: ", type(fps))
        total_recording_frames = np.ceil(
            float(recording_duration) * fps)  # Sometimes there's one extra frame in videos beyond the expected duration
        video_end_time = get_video_end_time(video_path + camera_dir)
        print("video_end_time: ", video_end_time)
        video_dfs[camera_dir] = pd.to_datetime(
            adjust_constant_frame_rate_timestamps(video_end_time, total_recording_frames, fps)['timestamp'])
    first_row_datetimes = list(video_dfs.iloc[:1].values)[0]
    print("first_row_datetimes: ", first_row_datetimes)
    latest_start_camera = list(video_dfs.columns)[first_row_datetimes.argmax()]
    latest_start_datetime = video_dfs[latest_start_camera].iloc[:1].values[0]
    print("\nlatest starting camera:", latest_start_camera, "\nat", latest_start_datetime)
    cams_index_closest_start_times = {}
    for camera_date_times in video_dfs.columns:
        if camera_date_times != latest_start_camera:
            cams_index_closest_start_times[camera_date_times] = \
                video_dfs[camera_date_times].searchsorted(
                    latest_start_datetime) + 1  # adjust for 1-n frame #s, rather than 0-based indexing
            print("latest_start_datetime: ", latest_start_datetime)
            print("video_dfs[camera_date_times].searchsorted(latest_start_datetime) + 1: ", video_dfs[camera_date_times].searchsorted(
                    latest_start_datetime) + 1)
            print("video_dfs[camera_date_times]: ", video_dfs[camera_date_times])
            
        else:
            cams_index_closest_start_times[camera_date_times] = 0
    return cams_index_closest_start_times


def trim_videos(video_dir, sorted_values):
    max_value = max(sorted_values)
    num_frames = 300
    for dirname in os.listdir(video_dir):
        print("dirname: ", dirname)
        # check if the filename is a file (not a subdirectory)
        if os.path.isdir(os.path.join(video_dir, dirname)):
            dirname = os.path.join(video_dir, dirname)
            for filename in os.listdir(dirname):
                filename = os.path.join(dirname, filename)
                print("filename: ", filename)
                if not filename.endswith('.avi'):
                    continue
                new_filename = os.path.join(video_dir, dirname) + "_trimmed"
                print("new_filename: ", new_filename)
                if '0' in filename:
                    print("filename: ", filename)
                    curr_frame_val = sorted_values[0]
                    print("num_frames: ", num_frames)
                    start_frame = curr_frame_val
                    end_frame = num_frames - (max_value - curr_frame_val)
                    subprocess.run(
                        f"ffmpeg -ss 0 -i {filename} -vf \"trim=start_frame={start_frame}:end_frame={end_frame},setpts=PTS-STARTPTS\" -c:a copy {new_filename}.avi",
                        shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                    )
                elif '4' in filename:
                    print("filename: ", filename)
                    curr_frame_val = sorted_values[1]
                    print("num_frames: ", num_frames)
                    start_frame = curr_frame_val
                    end_frame = num_frames - (max_value - curr_frame_val)
                    subprocess.run(
                        f"ffmpeg -ss 0 -i {filename} -vf \"trim=start_frame={start_frame}:end_frame={end_frame},setpts=PTS-STARTPTS\" -c:a copy {new_filename}.avi",
                        shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                    )
                elif '8' in filename:
                    print("filename: ", filename)
                    curr_frame_val = sorted_values[2]
                    # num_frames = subprocess.run(
                    #     f"ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames -of default=nokey=1:noprint_wrappers=1 {filename}"
                    # )
                    # print("num_frames: ", num_frames)
                    start_frame = curr_frame_val
                    end_frame = num_frames - (max_value - curr_frame_val)
                    subprocess.run(
                        f"ffmpeg -ss 0 -i {filename} -vf \"trim=start_frame={start_frame}:end_frame={end_frame},setpts=PTS-STARTPTS\" -c:a copy {new_filename}.avi",
                        shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                    )


def split_videos(video_dir, sorted_values):
    max_value = max(sorted_values)
    num_frames = 300
    for dirname in os.listdir(video_dir):
        print("dirname: ", dirname)
        # check if the filename is a file (not a subdirectory)
        if os.path.isdir(os.path.join(video_dir, dirname)):
            dirname = os.path.join(video_dir, dirname)
            for filename in os.listdir(dirname):
                filename = os.path.join(dirname, filename)
                print("filename: ", filename)
                if not filename.endswith('.avi'):
                    continue
                new_filename = os.path.join(video_dir, dirname) + "_trimmed"
                print("new_filename: ", new_filename)
                if '0' in filename:
                    print("filename: ", filename)
                    curr_frame_val = sorted_values[0]
                    print("num_frames: ", num_frames)
                    start_frame = curr_frame_val
                    end_frame = num_frames - (max_value - curr_frame_val)
                    subprocess.run(
                        f"ffmpeg -ss 0 -i {filename} -vf \"trim=start_frame={start_frame}:end_frame={end_frame},setpts=PTS-STARTPTS\" -c:a copy {new_filename}.avi",
                        shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                    )
                elif '4' in filename:
                    print("filename: ", filename)
                    curr_frame_val = sorted_values[1]
                    print("num_frames: ", num_frames)
                    start_frame = curr_frame_val
                    end_frame = num_frames - (max_value - curr_frame_val)
                    subprocess.run(
                        f"ffmpeg -ss 0 -i {filename} -vf \"trim=start_frame={start_frame}:end_frame={end_frame},setpts=PTS-STARTPTS\" -c:a copy {new_filename}.avi",
                        shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                    )
                elif '8' in filename:
                    print("filename: ", filename)
                    curr_frame_val = sorted_values[2]
                    # num_frames = subprocess.run(
                    #     f"ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames -of default=nokey=1:noprint_wrappers=1 {filename}"
                    # )
                    # print("num_frames: ", num_frames)
                    start_frame = curr_frame_val
                    end_frame = num_frames - (max_value - curr_frame_val)
                    subprocess.run(
                        f"ffmpeg -ss 0 -i {filename} -vf \"trim=start_frame={start_frame}:end_frame={end_frame},setpts=PTS-STARTPTS\" -c:a copy {new_filename}.avi",
                        shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                    )



if __name__ == "__main__":
    fps = 30
    video_path = 'C:/Users/User/CSE600/videos/11-17-22/output_videos/'
    cams_index_closest_start_times = get_start_indices_close_to_latest_camera(video_path, fps)
    sorted_keys = sorted(cams_index_closest_start_times.keys())
    sorted_values = [cams_index_closest_start_times[key] for key in sorted_keys]
    print("sorted_values: ", sorted_values)
    concat_videos_path = 'C:/Users/User/CSE600/videos/11-17-22/output_videos'
    trim_videos(concat_videos_path, sorted_values)