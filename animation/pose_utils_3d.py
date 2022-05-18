# %%
# @Author  : Gabrielle Strandquist, Tanner Dixon, Tomek Fraczek
# @Time    : 1/11/22 5:55 AM

##############################
# imports
import json, sys, datetime, os, fnmatch, hashlib, re, glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import butter, filtfilt


# def load_file(filename):
#     return pd.read_csv(filename, index_col=[0], header=[0, 1, 2, 3])


# def select_time(base_path, files, start_secs, end_secs, bonus):
#     video_fps = 30.0
#     start_frame = int(((start_secs-bonus) * video_fps)) - 1
#     end_frame = int(((end_secs+bonus) * video_fps)) + 1

#     if isinstance(files, str):
#         pose_data = load_file(os.path.join(base_path, files))
#     else:
#         multifile = [load_file(os.path.join(base_path, f)) for f in files]
#         pose_data = pd.concat(multifile, ignore_index=True)
#         # print(len(pose_data))
#     selected = pose_data.iloc[start_frame:end_frame]
#     return selected


# def conf_select(data, xyc_select, threshold=0.75):
#     all_data = data[xyc_select]
#     selection = all_data['c'] > threshold
#     return all_data.index, all_data[['x', 'y', 'z']], all_data['c']


# def index_to_time(indices):
#     return np.array(indices) / 30.0


def convert_openpose_csv_frame(csv_data, idx):
    print("IN CONVERT_OPENPOSE_CSV_FRAME! and the idx is: ", idx)
    chunked_list = []
    cols_list = ['Body', 'L Hand', 'R Hand', 'Face']
    for i, col_name in enumerate(cols_list):
        points_list = list(csv_data.loc[csv_data.index[idx], col_name])
        print("points_list: ", points_list)
        if col_name == 'Body':
            chunked_list = chunked_list \
                           + [points_list[i:i + 4]
                              for i in range(0, len(points_list) - 4, 4)] #skip the "background" key points for now
        else:
            chunked_list = chunked_list \
                          + [points_list[i:i + 4]
                             for i in range(0, len(points_list), 4)]
        print("chunked_list: ", chunked_list)
    return chunked_list


# #####################
# Functions for pose segments
def draw_body_segment(frame_data, kp_idx, ax):
    # extract the appropriate segment (pair of keypoints)
    segment_data = [frame_data[i] for i in kp_idx]
    print("segment_data: ", segment_data)
    # assign color: left side body is blue, right is red, midline is purple
    left_idx = [5, 6, 7, 12, 13, 14, 16, 18, 19, 20, 21] \
                + [i + 25 for i in range(21)]
    right_idx = [2, 3, 4, 9, 10, 11, 15, 17, 22, 23, 24] \
                 + [i + 46 for i in range(21)]
    if any(kp in kp_idx for kp in left_idx):
        clr = 'b'
    elif any(kp in kp_idx for kp in right_idx):
        clr = 'r'
    else:
        clr = 'm'
    # hide the segment off screen if the confidence is too low for either kp
    if (segment_data[0][2] < 0.1) or (segment_data[1][2] < 0.1):
        x = [10, 10]
        y = [10, 10]
        z = [10, 10]
    else:
        print("segment_data[0]: ", segment_data[0])
        x = [segment_data[0][0], segment_data[1][0]]
        y = [-1 * segment_data[0][1], -1 * segment_data[1][1]]
        z = [segment_data[0][2], segment_data[1][2]]
    # plot the segment
    segment = ax.plot3D(x, y, z, clr + 'o-')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    print("segment: ", segment[0].get_data_3d())

    return segment


def update_body_segment(frame_data, kp_idx, segment):
    # extract the appropriate segment (pair of keypoints)
    segment_data = [frame_data[i] for i in kp_idx]
    # hide the segment off screen if the confidence is too low for either kp
    if (segment_data[0][2] < 0.1) or (segment_data[1][2] < 0.1):
        x = [10, 10]
        y = [10, 10]
        z = [10, 10]
    else:
        x = [segment_data[0][0], segment_data[1][0]]
        y = [-1 * segment_data[0][1], -1 * segment_data[1][1]]
        z = [-1 * segment_data[0][2], -1 * segment_data[1][2]]
    # update the segment data
    segment.set_data_3d(x, y, z)
    print("UDPATED SEGMENT: ", segment.get_data_3d())


def draw_body_frame(segments, kp_df_row, ax):
    # convert the df row to a list
    frame_data = kp_df_row.values.tolist()
    # define each pair of keypoints to be plotted with connections
    kp_idx_pairs = [[17, 15],  # pose
                    [15, 0],
                    [0, 16],
                    [16, 18],
                    [0, 1],
                    [4, 3],
                    [3, 2],
                    [2, 1],
                    [1, 5],
                    [5, 6],
                    [6, 7],
                    [1, 8],
                    [23, 22],
                    [22, 11],
                    [11, 24],
                    [11, 10],
                    [10, 9],
                    [9, 8],
                    [8, 12],
                    [12, 13],
                    [13, 14],
                    [14, 21],
                    [14, 19],
                    [19, 20],
                    [25, 30],  # left hand
                    [25, 34],
                    [25, 38],
                    [25, 42],
                    [46, 51],  # right hand
                    [46, 55],
                    [46, 59],
                    [46, 63],
                    ] \
                   + [[i + 25, i + 26] for i in
                      [0, 1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19]] \
                   + [[i + 46, i + 47] for i in
                      [0, 1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19]]

    # plot each visible body segment
    if len(segments) == 0:  # first frame
        for i, kp_idx in enumerate(kp_idx_pairs):
            segments.append(draw_body_segment(frame_data, kp_idx, ax))
        ax.set_xlim(-0.5, 0.5)  # 600 to 2500
        ax.set_ylim(-0.5, 0.5)  # -100 to 2000
        ax.set_zlim(-2, 2)  # 0 to 2000
        # ax.invert_xaxis()
        # ax.invert_yaxis()
        ax.set_aspect("auto")
    else:  # subsequent frames
        for i, kp_idx in enumerate(kp_idx_pairs):
            update_body_segment(frame_data, kp_idx, segments[i][0])

    return segments


def process_pose_csvs(vid_start_time, vid_end_time, pose_file):
    chunked_kp_list = list()
    csv_data = pd.read_csv(pose_file, header=[0, 1, 2, 3])
    print("csv_data: ", csv_data)
    print("parsing csv...")
    for idx in range(0, 518):
        chunked_kp_list.append(convert_openpose_csv_frame(csv_data, idx))
    kp_df = pd.DataFrame(chunked_kp_list)
    print("csv dataframe created!", len(chunked_kp_list))
    return kp_df


# def load_pose_file(filename):
#     return pd.read_csv(filename, index_col=[0], header=[0, 1, 2, 3])

