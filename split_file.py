import os
import re
import tkinter as tk
from tkinter import filedialog
from openpyxl import Workbook
from datetime import datetime
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        rawdata = file.read()
        result = chardet.detect(rawdata)
    return result['encoding']

def split_text_file(input_file, output_folder, num_splits, should_detect_encoding=False):
    encoding = None

    if should_detect_encoding:
        encoding = detect_encoding(input_file)

    # 打开输入文件
    with open(input_file, 'r', encoding=encoding) as file:
        lines = file.readlines()

    # 确定每个分割文件应包含的行数
    num_lines = len(lines)
    lines_per_split = num_lines // num_splits
    remainder = num_lines % num_splits

    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 分割文件
    start = 0
    for i in range(num_splits):
        end = start + lines_per_split
        if remainder > 0:
            end += 1
            remainder -= 1

        output_file = os.path.join(output_folder, f'split_{i + 1}.txt')
        with open(output_file, 'w', encoding=encoding) as out_file:
            out_file.writelines(lines[start:end])

        start = end

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    input_file = filedialog.askopenfilename()

    # 让用户选择是否进行编码检测
    should_detect_encoding = input("是否进行编码检测？(y/n): ").strip().lower() == 'y'

    #input_file = "input.txt"  # 输入文件的路径
    output_folder = "output"  # 分割文件的输出文件夹
    num_splits = 100  # 要分割的文件份数

    split_text_file(input_file, output_folder, num_splits, should_detect_encoding)


