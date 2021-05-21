import argparse
import glob
import re
import cv2
import os

numbers = re.compile(r'(\d+)')


def numerical_sort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


def make_video(frames):
    full_path = os.path.join(frames, '*.png')
    all_images = glob.glob(full_path)
    all_images = sorted(all_images, key=numerical_sort)
    img_array = []
    # print(all_images)
    for im in all_images:
        if 'mask' in im:
            all_images.remove(im)
    # print(all_images)

    for filename in all_images:
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)
    frames_name = os.path.basename(frames)
    out_file = os.path.join(r'./videos/{}.mp4'.format(frames_name))

    out = cv2.VideoWriter(out_file, cv2.VideoWriter_fourcc(*'MPEG'), 22, size)
    for i in img_array:
        out.write(i)
    out.release()


def make_several_videos(folder):
    sub_dirs = [x[0] for x in os.walk(folder)]
    sub_dirs.remove(folder)
    for frames in sub_dirs:
        print('Working on {}'.format(os.path.basename(frames)))
        full_path = os.path.join(frames, '*.png')
        all_images = glob.glob(full_path)
        all_images = sorted(all_images, key=numerical_sort)
        img_array = []
        # print(all_images)
        for im in all_images:
            if 'mask' in im:
                all_images.remove(im)
        # print(all_images)

        for filename in all_images:
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width, height)
            img_array.append(img)
        frames_name = os.path.basename(frames)
        out_file = os.path.join(r'./videos/{}.mp4'.format(frames_name))

        out = cv2.VideoWriter(out_file, cv2.VideoWriter_fourcc(*'MPEG'), 22, size)
        for i in img_array:
            out.write(i)
        out.release()


def extract_frames(video):
    video_name = os.path.basename(video)
    out_path = os.path.join(r'./video_frames/{}'.format(video_name[:-4]))
    if os.path.exists(out_path):
        files = glob.glob(os.path.join(out_path, '*.png'))
        for f in files:
            os.remove(f)
    else:
        os.makedirs(out_path)

    vidcap = cv2.VideoCapture(video)
    success, image = vidcap.read()
    count = 0
    while success:
        write_path = os.path.join(out_path, 'frame_%04d.png' % count)
        cv2.imwrite(write_path, image)
        success, image = vidcap.read()
        count += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Video processing')
    parser.add_argument('--video', type=str, default='', help='path and name of the video')
    parser.add_argument('--frames', type=str, default='',
                        help='path and folder name of frames')
    parser.add_argument('--frame_folders', type=str, default='',
                        help='path and folder names of frames')
    # Adding -- before an argument makes it optional else it will be a mandatory argument
    args = parser.parse_args()
    if args.frames != '':
        make_video(args.frames)
        '''
        To make a video:
        python video_processing.py --frames Folder_containing_the_frames
        '''
    elif args.video != '':
        extract_frames(args.video)
        '''
        To split a video in frames:
        python video_processing.py --video Path_to_the_video
        '''
    else:
        make_several_videos(args.frame_folders)
        '''
        To make several video:
        python video_processing.py --frame_folders Folder_containing_the_sub folder of frames
        '''