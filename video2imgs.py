
#coding=utf-8
import os

def find_mp4(mp4_path):
    mp4_files = []
    for each_file in os.listdir(mp4_path):
        # print(each_file)
        if each_file.split('.')[-1] == 'mp4':
            mp4_files.append(each_file)
    return mp4_files


def video2imgs():
    for i in range(1, 12):
        print('ffmpeg -i a{}.mp4 -r 1 a{}/a{}%d.jpg'.format(i, i, i))
        os.system('ffmpeg -i a{}.mp4 -r 1 a{}/a{}%d.jpg'.format(i, i, i))



for i in find_mp4(r'D:\multi_download_youtu_videos\riots'):
    print(i)