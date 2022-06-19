from re import I
import sys, os
from cv2 import threshold
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm
# import datetime as dt
from datetime import datetime 
from datetime import time


def get_time_increments(dir):
    max_timestamp = ''
    filenames = os.listdir(dir)
    first_timestamps = []
    os.chdir(dir)
    for i, filename in enumerate(filenames):
        df = pd.read_csv(filename)
        first_row = df.iloc[0]
        first_timestamp = first_row['cfr_estimate']
        # format after strptime: 2021-10-25T10:30:03.797292
        first_timestamp = datetime.strptime(first_timestamp, "%Y-%m-%dT%I:%M:%S.%f")
        first_timestamps.append(first_timestamp)

        if max_timestamp == '':
            max_timestamp = first_timestamp
        else:
            if first_timestamp > max_timestamp:
                max_timestamp = first_timestamp

    interval = 1000000/30
    microsecond_time_increments = []
    num_row_increments = []

    for first_timestamp in first_timestamps:
        diff = max_timestamp - first_timestamp

        total_microseconds = (diff.seconds * 1000000) + diff.microseconds
        microsecond_time_increments.append(total_microseconds)

        num_row_increment = total_microseconds / interval
        num_row_increments.append(num_row_increment)

    return microsecond_time_increments, num_row_increments

    

if __name__ == "__main__":
    args = sys.argv[1:]
    # pose_csv = r'C:\Users\User\CSE600\align-videos\cfr_timestamps_video0_2021-10-25.csv'

    dir = args[0]
    microsecond_time_increments, num_row_increments = get_time_increments(dir)
    print("microsecond_time_increments: ", microsecond_time_increments)
    print("num_row_increments: ", num_row_increments)


