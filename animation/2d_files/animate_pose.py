#####################
# Imports
import sys
import warnings
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib import animation, rcParams
from pose_utils import draw_body_frame, process_pose_csvs

rcParams['timezone'] = 'America/Los_Angeles'
rcParams['animation.embed_limit'] = 2**128
warnings.filterwarnings('ignore')


#####################
# Paths & vars
# pose_folder = r'D:\Neurohub Systems\DataNet\temp-data\20211117'
# pose_csv = r'D:\Neurohub Systems\DataNet\temp-data\raw_pose_json\20211117\pose_video0_2021-11-17-20-08-03.csv'
# pose_csv = r'C:\Users\User\CSE600\openpose\csv_files\pose_video0_2022-03-15-10-50-03.csv'
# pose_csv = r'C:\Users\User\CSE600\wasabi_videos\11-17-21_videos\11-17-21_video0_pose_2d.csv'
# pose_csv = r'C:\Users\User\CSE600\wasabi_videos\11-17-21_videos\pose_video0_2021-11-17-20-08-03.csv'
# pose_csv = r'C:\Users\User\CSE600\wasabi_videos\3-11-22_videos\pose_video0_2022-03-11-10-06-04.csv'
# pose_csv = r'C:\Users\User\CSE600\wasabi_videos\3-11-22_videos\03-11-22_video0_pose_2d_full_video_version.csv'
# pose_csv = r'C:\Users\User\CSE600\wasabi_videos\3-11-22_videos\pose_video0_2022-03-11-10-06-04.csv'
pose_csv = r'C:\Users\User\CSE600\wasabi_videos\3-11-22_videos\03-11-22_video0_pose_2d_video_version.csv'

def add_datetime(df, t_str):
    df['time_secs'] = pd.to_datetime(df[t_str], unit='ms') \
        .dt.tz_localize('UTC') \
        .dt.tz_convert('US/Pacific')
    return df


# #####################
# # Process pose data
start = 20
length = 2
frame_range = int(39.5*30), int(58*30)
kp_df = process_pose_csvs(*frame_range, pose_csv)


# # ##############################
# # set up plot, create segments
fig = plt.figure()
segments = list()
print("kp_df.iloc[0]: ", kp_df.iloc[0])
print("after printing")
segments = draw_body_frame(segments, kp_df.iloc[0], plt.gca())
ax_window = 6


def draw_frame_wrapper(frame, segments, kp_df, pose_ax):
    returns = draw_body_frame(segments, kp_df.iloc[frame], pose_ax)
    pose_ax.set_title(f'Frame: {frame_range[0] + frame:4}')
    return returns


anim_processed = animation.FuncAnimation(fig, draw_frame_wrapper,  fargs=(segments, kp_df, plt.gca()), frames=len(kp_df), interval=1000/30, blit=False)
# anim_processed.save('csv_pose_processed_tp.gif', fps=30) #interval=1000/30

plt.show()