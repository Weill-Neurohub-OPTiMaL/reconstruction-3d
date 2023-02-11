import json, pdb, datetime, os, fnmatch, hashlib, re, csv, cv2
import pandas as pd
import numpy as np
from raw_vid_utils import *
from datetime import timedelta


def get_timestamp_csv(video_path, json_path, save_path):
    meta_file = json.load(open(json_path))
    real_record_start_time = meta_file['recordStartTime']
    real_record_end_time = meta_file['recordEndTime']
    fps = int(meta_file['frame_rate'])
    recording_duration = int(meta_file['recording_sesh_len']) #in seconds
    num_frames = recording_duration*fps
    num_intervals = num_frames - 1

    #calculate estimated times per frame
    estimate_cfr_timestamp = est_cfr_timestamps(num_frames, fps)
    full_end_datetime = datetime.datetime.strptime(real_record_end_time.split("T")[0] + ' ' + real_record_end_time.split("T")[1], "%Y-%m-%d %H:%M:%S.%f")
    estimate_cfr_datetimestamp = [0]*len(estimate_cfr_timestamp)
    #Use estimated cfr times to decrement back from recordEndTime
    for i in range(len(estimate_cfr_timestamp)):
        estimate_cfr_datetimestamp[i] = decrement_by_framenum(full_end_datetime, estimate_cfr_timestamp[i])
    estimate_cfr_datetimestamp.reverse()
    print("estimate_cfr_datetimestamp type: ", type(estimate_cfr_datetimestamp))
    print("estimate_cfr_datetimestamp len: ", len(estimate_cfr_datetimestamp))
    # np.save(granger_lp+"estimate_cfr_times_" + recording_name + ".npy", estimate_cfr_datetimestamp)

    # Calculate range of time covered by calculated times, compare to expected range
    beginning = datetime.datetime.strptime(estimate_cfr_datetimestamp[0].split("T")[0] + ' ' + estimate_cfr_datetimestamp[0].split("T")[1], "%Y-%m-%d %H:%M:%S.%f")
    end = datetime.datetime.strptime(estimate_cfr_datetimestamp[-1].split("T")[0] + ' ' + estimate_cfr_datetimestamp[-1].split("T")[1], "%Y-%m-%d %H:%M:%S.%f")
    print("Time range covered by calculated cfr-times:",end - beginning)
    expected_range = (num_intervals / fps)
    print("Expected range:", timedelta(seconds=round((num_intervals / fps), 6)))

    with open(save_path, "w", newline="") as f:
        # Create a CSV writer
        writer = csv.writer(f)
        # Write the list of strings to the CSV file, one row at a time
        for string in estimate_cfr_datetimestamp:
            writer.writerow([string])


if __name__ == "__main__":
    video_path = 'C:/Users/User/CSE600/videos/full_2m/video8_2022-03-11-10-06-05.avi'
    json_path = 'C:/Users/User/CSE600/videos/full_2m/metadata_video8.json'
    save_path = 'C:/Users/User/CSE600/videos/full_2m/video8_2022-03-11-10-06-05.csv'
    get_timestamp_csv(video_path, json_path, save_path)