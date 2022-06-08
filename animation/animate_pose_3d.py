#####################
# Imports
import sys
import warnings
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import ctypes

from matplotlib import animation, rcParams
from pose_utils_3d import draw_body_frame, process_pose_csvs, open_video

rcParams['timezone'] = 'America/Los_Angeles'
rcParams['animation.embed_limit'] = 2**128
warnings.filterwarnings('ignore')


#####################
# Paths & vars
# pose_folder = r'D:\Neurohub Systems\DataNet\temp-data\20211117'
# pose_csv = r'D:\Neurohub Systems\DataNet\temp-data\raw_pose_json\20211117\pose_video0_2021-11-17-20-08-03.csv'
pose_csv = r'C:\Users\User\CSE600\wasabi_videos\3-11-22_videos\03-11-22_pose_3d.csv'

# def add_datetime(df, t_str):
#     df['time_secs'] = pd.to_datetime(df[t_str], unit='ms') \
#         .dt.tz_localize('UTC') \
#         .dt.tz_convert('US/Pacific')
#     return df


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
ax_3d = plt.axes(projection="3d")
segments = draw_body_frame(segments, kp_df.iloc[0], ax_3d)
ax_window = 6

cap = cv2.VideoCapture(r"C:\Users\User\CSE600\wasabi_videos\11-17-21_videos\video0_2021-11-17-20-08-03_10s.mov")
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def draw_frame_wrapper(frame, segments, kp_df, pose_ax):
    if int(frame/90) % 2 == 0:
        azim_val = frame%90
    else:
        azim_val = 90-(frame%90)
    pose_ax.view_init(elev=azim_val, azim=180+frame)
    # plt.pause(.1)
    returns = draw_body_frame(segments, kp_df.iloc[frame], pose_ax)
    # angle += 0
    pose_ax.set_title(f'Frame: {frame_range[0] + frame:4}')
    
    display_video()

    return returns


def display_video():
    ret, frame = cap.read()
    if frame is None:
        cap.release()
        cv2.destroyAllWindows()
        return
    width = int(frame.shape[1] * (50 / 100))
    height = int(frame.shape[0] * (50 / 100))
    dim = (width, height)
    resized = cv2.resize(frame, dim)
    # moved = cv2.moveWindow("frame", int(screensize[0] - (screensize[0] * 0.5)), int(screensize[1] - (screensize[1] * 0.5)))
    cv2.imshow('frame', resized)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        return



# open_video(r"C:\Users\User\CSE600\wasabi_videos\11-17-21_videos\video0_2021-11-17-20-08-03_10s.mov")
anim_processed = animation.FuncAnimation(fig, draw_frame_wrapper, fargs=(segments, kp_df, ax_3d), frames=len(kp_df), interval=1000/30, blit=False)
# anim_processed.save('csv_pose_processed_tp.gif', fps=30) #interval=1000/30

plt.show()