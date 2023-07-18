# -*- coding: utf-8 -*-

import os
import glob
from handler import *

os.makedirs('output', exist_ok=True)
os.makedirs('tmp', exist_ok=True)

def main():
    # 使用方法
    pdf_paths = glob.glob('input/*.pdf')  # 需要压缩的 PDF 文件路径
    output_paths = list(map(lambda x: x.replace('input', 'output'), pdf_paths))  # 压缩后的 PDF 文件路径


    for i, pdf_path in enumerate(pdf_paths):
        print(f'Before process {pdf_path}')
        image_paths = extract_images_from_pdf(pdf_path)
        print(f'Extract all images {image_paths} from {pdf_path}')
        images_to_pdf(image_paths, output_paths[i])
        print(f'Finish compress all images {image_paths} to {output_paths[i]}')

        # 删除临时文件
        for path in image_paths:
            os.remove(path)

if __name__ == '__main__':
    main()
