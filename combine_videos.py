# 组合mp4和ogg
# 一个Python程序，从指定文件夹遍历文件夹和子文件夹内的所有mp4和ogg文件，并将对应的mp4和ogg文件使用ffmpeg-python组合输出到另一个文件夹。
# 判断文件对应的方法是，从文件名的开始到结尾，逐字比对文件名是否相同，如果出现不相同，文件名最相同的mp4和ogg为对应。
# 需要注意，对应的mp4和ogg文件不一定在同一个文件夹中。
# 需要ffmpeg在PATH内
import logging
import os
import shutil
import sys
import subprocess

# set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s.%(funcName)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def find_matching_files(path):
    mp4_files = []
    ogg_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.mp4'):
                mp4_files.append(os.path.join(root, file))
            elif file.endswith('.ogg'):
                ogg_files.append(os.path.join(root, file))
    return mp4_files, ogg_files


def match_files(mp4_files, ogg_files):
    matched_pairs = []
    for mp4_file in mp4_files:
        best_match = None
        best_score = 0
        for ogg_file in ogg_files:
            score = 0
            mp4_filename = os.path.basename(mp4_file)
            ogg_filename = os.path.basename(ogg_file)
            max_len = max(len(mp4_filename), len(ogg_filename))
            mp4_filename = mp4_filename.ljust(max_len, "V")
            ogg_filename = ogg_filename.replace(
                "Sound", "Video").ljust(max_len, "A")
            # print(ogg_filename)
            for i in range(max_len):
                if mp4_filename[i] == ogg_filename[i]:
                    score += 1
                else:
                    break
            if score > best_score:
                best_match = ogg_file
                best_score = score
        if best_score > 0:
            matched_pairs.append((mp4_file, best_match, best_score))
            logging.info(
                f'Found {best_match} for {mp4_file}, score {best_score}')
        else:
            matched_pairs.append((mp4_file, False, best_score))
            logging.info(f'No best match for {mp4_file}')
    return matched_pairs


def combine_and_output(matched_pairs, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    for pair in matched_pairs:
        if pair[1]:
            # input_mp4 = ffmpeg.input(pair[0])
            # input_ogg = ffmpeg.input(pair[1])
            output_name = os.path.basename(pair[0]).split('.')[0] + '.mp4'
            os.chdir(output_path)
            if not os.path.exists(output_name):
                output_path_full = os.path.join(output_path, output_name)
                # another way to process video and vocal
                input_mp4 = pair[0]
                input_ogg = pair[1]
                cmd = f'ffmpeg -i {input_mp4} -i {input_ogg} -loglevel quiet -acodec copy -vcodec copy {output_path_full}'
                logging.info(
                    f'Combining {pair[0]} and {pair[1]} to {output_path_full}')
                try:
                    (
                        # ffmpeg.concat(input_mp4, input_ogg, v=1, a=1)
                        # .output(output_path_full)
                        # .run()
                        subprocess.call(cmd)
                    )
                except Exception as e:
                    import traceback
                    logging.error(traceback.format_exc())
            else:
                continue
        else:
            input_mp4 = pair[0]
            output_name = os.path.basename(pair[0]).split('.')[0] + '.mp4'
            output_path_full = os.path.join(output_path, output_name)
            shutil.copy(input_mp4, output_path_full)
            logging.info(f'Copying {pair[0]} to {output_path_full}')


source_path = sys.path[0]
path_to_search = source_path + r'/ba_jp_media'
output_path = source_path + r'/ba_jp_media_combined'

mp4_files, ogg_files = find_matching_files(path_to_search)
matched_pairs = match_files(mp4_files, ogg_files)
combine_and_output(matched_pairs, output_path)
