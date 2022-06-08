from re import I
import sys
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm

kp_idx_pairs = [
    [0, 15], [0, 16], [15, 17], [16, 18], 
    [1, 2], [1, 5], [2, 3], [5, 6], 
    [3, 4], [6, 7], [8, 9], [8, 12], 
    [9, 10], [12, 13], [10, 11], [13, 14], 
    [11, 24], [14, 21], [11, 22], [14, 19], 
    [22, 23], [19, 20], [0, 1], [1, 8]
    ] 

distances = [
    [], [], [], [], 
    [], [], [], [], 
    [], [], [], [], 
    [], [], [], [], 
    [], [], [], [], 
    [], [], [], []
    ]

distance_labels = [
    'nose to right eye', 'nose to left eye', 'right eye to ear', 'left eye to ear', 
    'chest to right shoulder', 'chest to left shoulder', 'right shoulder to elbow', 'left shoulder to elbow', 
    'right elbow to wrist', 'left elbow to wrist', 'waist to right hip', 'waist to left hip', 
    'right hip to knee', 'left hip to knee', 'right knee to ankle', 'left knee to ankle', 
    'right ankle to heel', 'left ankle to heel', 'right ankle to big toe', 'left ankle to big toe', 
    'right big toe to little toe', 'left big toe to little toe', 'nose to chest', 'chest to waist'
    ]

distance_labels_pairs = []

colors = [
    'b', 'g', 'r', 'c', 
    'm', 'k', 'y', 'lime', 
    'darkorange', 'gold', 'rosybrown', 'peru', 
    'dimgray', 'blueviolet', 'pink', 'olive',
    'cyan', 'mediumaquamarine', 'hotpink', 'navajowhite',
    'limegreen', 'lightskyblue', 'navy', 'maroon'
    ]

# colors = cm.rainbow(np.linspace(0, 1, len(kp_idx_pairs)))

def process_pose_csvs(pose_file):
    chunked_kp_list = list()
    csv_data = pd.read_csv(pose_file, header=[0, 1, 2, 3])
    print("csv_data: ", csv_data)
    print("parsing csv...")
    for idx in range(csv_data.shape[0]):
        chunked_kp_list.append(convert_openpose_csv_frame(csv_data, idx))
    kp_df = pd.DataFrame(chunked_kp_list)
    return kp_df


def convert_openpose_csv_frame(csv_data, idx):
    chunked_list = []
    cols_list = ['Body']
    for i, col_name in enumerate(cols_list):
        points_list = list(csv_data.loc[csv_data.index[idx], col_name])
        chunked_list = chunked_list \
                        + [points_list[i:i + 4]
                            for i in range(0, len(points_list) - 4, 4)] #skip the "background" key points for now
    return chunked_list


def get_euclidean_distance(x1, y1, z1, x2, y2, z2):
    return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2) + ((z2 - z1) ** 2))


def calculate_distances_single_row(kp_df_row):
    for i, pair in enumerate(kp_idx_pairs):
        idx_1 = pair[0]
        idx_2 = pair[1]
        point_1 = kp_df_row[idx_1]
        point_2 = kp_df_row[idx_2]
        if point_1[3] != 0 and point_2[3] != 0:
            dist = get_euclidean_distance(point_1[0], point_1[1], point_1[2], point_2[0], point_2[1], point_2[2])
            distances[i].append(dist)


def calculate_distances(kp_df):
    for i in range(kp_df.shape[0]):
        calculate_distances_single_row(kp_df.iloc[i])


def calculate_average_distances():
    average_distances = []
    for distance_lst in distances:
        if len(distance_lst) == 0:
            average_distances.append(0)
        else:
            average_distances.append(sum(distance_lst) / len(distance_lst))

    return average_distances


def sort_by_average_distances(average_distances):
    sorted_kp_idx_pairs = [i for _,i in sorted(zip(average_distances, kp_idx_pairs))]
    sorted_distance_labels = [i for _,i in sorted(zip(average_distances,distance_labels))]
    sorted_distances = [i for _,i in sorted(zip(average_distances,distances))]

    return sorted_kp_idx_pairs, sorted_distance_labels, sorted_distances


def plot_std_devs(average_distances, kp_df, csv_date, frame_rate, 
sorted_kp_idx_pairs, sorted_distance_labels, sorted_distances, fig_num):

    skipped = 0
    not_skipped = 0

    thresh = 0.75
    plt.figure(fig_num)
    plt.title("Standard Deviations for 3D Distances for %i s video on date %s (%i keypoints at %i fps)" % 
        (kp_df.shape[0]//float(frame_rate), csv_date, kp_df.shape[0], int(frame_rate)))
    plt.xlabel("Body Parts")
    plt.ylabel("Standard Deviation")
    average_distances.sort()
    x = []
    y = []
    for i in range(int(len(sorted_kp_idx_pairs))):
        if len(sorted_distances[i]) < (thresh*kp_df.shape[0]):
            skipped += 1
            continue
        x.append(sorted_distance_labels[i])
        y.append(np.std(sorted_distances[i]))
        not_skipped += 1
    print("before plt.bar")
    print("x in bar: ", x)
    print("y in bar: ", y)
    plt.bar(x, y, color='lightpink')
    plt.xticks(rotation=30)
    # plt.show()

    print("skipped: ", skipped)
    print("not skipped: ", not_skipped)


def plot_lines_split_graphs(kp_df, csv_date, frame_rate, 
sorted_kp_idx_pairs, sorted_distance_labels, sorted_distances, fig_num):
    
    skipped = 0
    not_skipped = 0

    thresh = 0.75
    num_distances_per_graph = 2
    num_graphs = len(kp_idx_pairs)/num_distances_per_graph
    subplot_len = 4
    subplot_width = num_graphs//subplot_len
    plt.figure(fig_num)
    fig, axs = plt.subplots(int(subplot_len), int(subplot_width))
    fig.suptitle("3D Distances for %i s video on date %s (%i keypoints at %i fps)" % 
        (kp_df.shape[0]//float(frame_rate), csv_date, kp_df.shape[0], int(frame_rate)))
    fig.supxlabel("Time (1/30th sec)")
    fig.supylabel("Euclidean Distance Between Body Part (meters)")
    for i in range(int(len(sorted_kp_idx_pairs)/num_distances_per_graph)):
        x_grid_idx = int(i/subplot_width)
        y_grid_idx = int(i%subplot_width)
        legend_list = []
        for j in range(num_distances_per_graph):
            curr_index = (num_distances_per_graph*i)+j
            if len(sorted_distances[curr_index]) < (thresh*kp_df.shape[0]):
                skipped += 1
                continue
            x = np.arange(1, len(sorted_distances[curr_index])+1)
            y = sorted_distances[curr_index]
            axs[x_grid_idx, y_grid_idx].plot(x, y, color=colors[curr_index])
            legend_list.append(sorted_distance_labels[curr_index])
            not_skipped += 1
        axs[x_grid_idx, y_grid_idx].legend(legend_list)

    print("skipped: ", skipped)
    print("not skipped: ", not_skipped)

    # plt.show()


def plot_single_histogram(kp_df, csv_date, frame_rate, 
sorted_kp_idx_pairs, sorted_distance_labels, sorted_distances, fig_num):

    skipped = 0
    not_skipped = 0

    thresh = 0.75
    plt.figure(fig_num)
    plt.title("3D Distances for %i s video on date %s (%i keypoints at %i fps)" % 
        (kp_df.shape[0]//float(frame_rate), csv_date, kp_df.shape[0], int(frame_rate)))
    plt.xlabel("Euclidean Distance Between Body Part (meters)")
    plt.ylabel("Count of Keypoints")
    legend_list = []
    for i in range(int(len(sorted_kp_idx_pairs))):
        if len(sorted_distances[i]) < (thresh*kp_df.shape[0]):
            skipped += 1
            continue
        y = sorted_distances[i]
        plt.hist(y, color=colors[i], alpha=0.75)
        not_skipped += 1
        legend_list.append(sorted_distance_labels[i])
    plt.legend(legend_list)

    print("skipped: ", skipped)
    print("not skipped: ", not_skipped)

    # plt.show()


def plot_histograms_split_graphs(kp_df, csv_date, frame_rate, 
sorted_kp_idx_pairs, sorted_distance_labels, sorted_distances, fig_num):

    skipped = 0
    not_skipped = 0

    thresh = 0.75
    num_distances_per_graph = 2
    num_graphs = len(kp_idx_pairs)/num_distances_per_graph
    subplot_len = 4
    subplot_width = num_graphs//subplot_len
    plt.figure(fig_num)
    fig, axs = plt.subplots(int(subplot_len), int(subplot_width))
    fig.suptitle("3D Distances for %i s video on date %s (%i keypoints at %i fps)" % 
        (kp_df.shape[0]//float(frame_rate), csv_date, kp_df.shape[0], int(frame_rate)))
    fig.supxlabel("Euclidean Distance Between Body Part (meters)")
    fig.supylabel("Count of Keypoints")
    for i in range(int(len(sorted_kp_idx_pairs)/num_distances_per_graph)):
        x_grid_idx = int(i/subplot_width)
        y_grid_idx = int(i%subplot_width)
        legend_list = []
        for j in range(num_distances_per_graph):
            curr_index = (num_distances_per_graph*i)+j
            if len(sorted_distances[curr_index]) < (thresh*kp_df.shape[0]):
                skipped += 1
                continue
            y = sorted_distances[curr_index]
            axs[x_grid_idx, y_grid_idx].hist(y, color=colors[curr_index], alpha=0.75)
            legend_list.append(sorted_distance_labels[curr_index])
            not_skipped += 1
        axs[x_grid_idx, y_grid_idx].legend(legend_list)

    print("skipped: ", skipped)
    print("not skipped: ", not_skipped)

    # plt.show()


def plot_histograms_opposite_pairs(kp_df, csv_date, frame_rate, fig_num):

    skipped = 0
    not_skipped = 0

    thresh = 0.75
    num_distances_per_graph = 2
    num_graphs = len(kp_idx_pairs)/num_distances_per_graph
    subplot_len = 4
    subplot_width = num_graphs//subplot_len
    # plt.figure(fig_num)
    fig, axs = plt.subplots(int(subplot_len), int(subplot_width))
    fig.suptitle("3D Distances for %i s video on date %s (%i keypoints at %i fps)" % 
        (kp_df.shape[0]//float(frame_rate), csv_date, kp_df.shape[0], int(frame_rate)))
    fig.supxlabel("Euclidean Distance Between Body Part (meters)")
    fig.supylabel("Count of Keypoints")
    for i in range(int(len(kp_idx_pairs)/num_distances_per_graph)):
        x_grid_idx = int(i/subplot_width)
        y_grid_idx = int(i%subplot_width)
        legend_list = []
        for j in range(num_distances_per_graph):
            curr_index = (num_distances_per_graph*i)+j
            # if len(distances[curr_index]) < (thresh*kp_df.shape[0]):
            #     skipped += 1
            #     continue
            y = distances[curr_index]
            axs[x_grid_idx, y_grid_idx].hist(y, color=colors[curr_index], alpha=0.75)
            legend_list.append(distance_labels[curr_index])
            not_skipped += 1
        axs[x_grid_idx, y_grid_idx].legend(legend_list)

    print("skipped: ", skipped)
    print("not skipped: ", not_skipped)

    # plt.show()


if __name__ == "__main__":
    args = sys.argv[1:]
    pose_csv = args[0]
    csv_date = args[1]
    frame_rate = args[2]
    # pose_csv = r'C:\Users\User\CSE600\reconstruction-3d\animation\3d_keypoints\3-11-22_3d.csv'

    fig_counter = 1

    kp_df = process_pose_csvs(pose_csv)
    calculate_distances(kp_df)
    average_distances = calculate_average_distances()
    sorted_kp_idx_pairs, sorted_distance_labels, sorted_distances = sort_by_average_distances(average_distances)

    plot_single_histogram(kp_df, csv_date, frame_rate, 
    sorted_kp_idx_pairs, sorted_distance_labels, sorted_distances, fig_counter)
    fig_counter += 1

    # plot_lines_split_graphs(kp_df, csv_date, frame_rate, 
    # sorted_kp_idx_pairs, sorted_distance_labels, sorted_distances, 1)
    # plot_histograms_split_graphs(kp_df, csv_date, frame_rate, 
    # sorted_kp_idx_pairs, sorted_distance_labels, sorted_distances, 2)
    # fig_coutner += 1

    plot_histograms_opposite_pairs(kp_df, csv_date, frame_rate, fig_counter)
    fig_counter += 1

    plot_std_devs(average_distances, kp_df, csv_date, frame_rate, 
    sorted_kp_idx_pairs, sorted_distance_labels, sorted_distances, fig_counter)
    fig_counter += 1

    plt.show()

