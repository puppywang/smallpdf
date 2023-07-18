# -*- coding: utf-8 -*-


from pdf2image import convert_from_path
import img2pdf
import os
from PyPDF2 import PdfReader


def get_page_size(pdf_path, page_number):
    reader = PdfReader(pdf_path)
    page = reader.pages[page_number]
    width = page.mediabox.width
    height = page.mediabox.height
    rotate = page.get('/Rotate', 0)
    if rotate in [90, 270]:
        width, height = height, width
    return int(round(width)), int(round(height))

# 从 PDF 文件中提取图像
def extract_images_from_pdf(pdf_path, quality):
    images = convert_from_path(pdf_path, dpi=150)  # 降低分辨率
    image_paths = []
    page_sizes = []
    for i, image in enumerate(images):
        width, height = get_page_size(pdf_path, i)
        image_path = os.path.join('tmp', 'image_{}.jpg'.format(i))  # 使用 JPEG 格式
        image.save(image_path, 'JPEG', quality=quality)  # 提高压缩级别
        image_paths.append(image_path)
        page_sizes.append((width, height))  # add the size of the page
    return image_paths, page_sizes

# 将图像嵌入到 PDF 文件中
def images_to_pdf(image_paths, pdf_path, page_sizes):
    with open(pdf_path, 'wb') as f:
        f.write(img2pdf.convert(image_paths, with_pdfrw=False, dpi=150, layout_fun=img2pdf.get_layout_fun(page_sizes[0])))
