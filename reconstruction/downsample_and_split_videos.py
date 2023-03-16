import sys
import os


def downsample_videos(video_dir, output_dir, cam_num):
    os.chdir(video_dir)
    for filename in sorted(os.listdir(video_dir)):
        if not filename.endswith('.avi'):
            continue
        print("filename: ", filename)
        downsample_cmd = 'ffmpeg -i ' + video_dir + filename + ' -vf scale=1920:1080 -c mjpeg ' + output_dir + filename[0:-4] + "_HD.avi"
        print("downsample_cmd: ", downsample_cmd)
        os.system(downsample_cmd)


def split_videos(video_dir, output_dir, cam_num):
    start_num = 0
    for filename in sorted(os.listdir(video_dir)):
        if not filename.endswith('.avi'):
            continue
        print("filename: ", filename)
        os.chdir(output_dir)
        split_cmd = 'ffmpeg -i ' + video_dir + filename + ' -vcodec copy -start_number ' + str(start_num) + ' cam' + str(cam_num) + '_%06d.jpg'
        print("split_cmd: ", split_cmd)
        os.system(split_cmd)
        os.chdir(video_dir)
        print("start_num: ", start_num)
        start_num += 3600


if __name__ == "__main__":
    # video_dir is the directory with all of the 2 min videos
    # output_dir is the directory that we want to output all images into
    #video_dir = sys.argv[1]
    #output_dir = sys.argv[2]
    #cam_num = sys.argv[3]

    '''
    video_dir = '/storage/20211117/video0_2021-11-17T20:00:00.011614/'
    output_dir = '/storage/20211117/video0_2021-11-17T20:00:00.011614_HD/'
    cam_num = 0
    #split_videos(video_dir, output_dir, cam_num)
    downsample_videos(video_dir, output_dir, cam_num)
    video_dir = '/storage/20211117/video4_2021-11-17T20:00:00.011614/'
    output_dir = '/storage/20211117/video4_2021-11-17T20:00:00.011614_HD/'
    cam_num = 4
    downsample_videos(video_dir, output_dir, cam_num)
    video_dir = '/storage/20211117/video8_2021-11-17T20:00:00.011615/'
    output_dir = '/storage/20211117/video8_2021-11-17T20:00:00.011615_HD/'
    cam_num = 8
    downsample_videos(video_dir, output_dir, cam_num)
    '''

    split_videos('/storage/20211117/video0_2021-11-17T20:00:00.011614_HD/', '/storage/20211117/combined_HD_images/', 0)
    split_videos('/storage/20211117/video4_2021-11-17T20:00:00.011614_HD/', '/storage/20211117/combined_HD_images/', 4)
    split_videos('/storage/20211117/video8_2021-11-17T20:00:00.011615_HD/', '/storage/20211117/combined_HD_images/', 8)


