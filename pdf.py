from sys import path
from pdfrw import PdfReader, PdfWriter
import os
from datetime import datetime
import fitz

def split_pdf(file_path, output_dir = None):
    if not os.path.exists(file_path):
        print(f"{file_path} does not exist")
        return

    pages = PdfReader(file_path).pages
    file_name = os.path.basename(file_path).split('.')[0]

    if not output_dir:
        output_dir = os.path.dirname(file_path) + '/' + file_name

    os.makedirs(output_dir, exist_ok=True)

    for part in range(0, len(pages)):
        outdata = PdfWriter(f'{output_dir}/{file_name}_{part}.pdf')
        outdata.addpage(pages[part])
        outdata.write()
    
    print("split pdf done")

# 重新编号命名，step = 2
def split_pdf_with_step(file_path1, file_path2):
    # file_path1 拆分后的 pdf 根据原文件名最后的数字大小正序递增，1,3,5

    # file_path2 拆分后的 pdf 根据原文件名最后的数字大小倒序递增，2,4,6，即原先数字最大的，新命名后的数字最小

    pass

def combind_single_pdf_(dir_name1, dir_name2, output_dir = None):
    # dir_name1 和 dir_name2 中的文件正序排列
    # 每次分别从 dir_name1 和 dir_name2 取一个文件写到新的 pdf

    pass

def combine_pdf_2(file_path1, file_path2, output_dir = None):
    if not os.path.exists(file_path1) or not os.path.exists(file_path2):
        print("file path does not exist")
        return
    
    reader1 = PdfReader(file_path1)
    reader2 = PdfReader(file_path2)

    pages1 = reader1.pages
    pages2 = reader2.pages

    if len(pages1) != len(pages2):
        print("warning: pages length is not equal")
        return

    if not output_dir:
        output_dir = os.path.dirname(file_path1)

    os.makedirs(output_dir, exist_ok=True)

    now = datetime.now()  # current date and time
    timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")

    output_path = f"{output_dir}/combined-output-{timestamp}.pdf"

    writer = PdfWriter(output_path)

    for i in range(0, len(pages1)):

        # 正序
        writer.addpage(pages1[i])

        # 倒序
        writer.addpage(pages2[len(pages2) - i - 1])

        writer.write()

    print(f'combine_pdf_2, output_path={output_path}')


def combine_pdf(input_dir, prefix, parts = [0, 1]):

    # os.makedirs(output_dir, exist_ok=True)

    output_path = f"{input_dir}/combine_{parts[0]}_{parts[1]}.pdf"

    outdata = PdfWriter(output_path)
    for i in range(parts[0], parts[1]):
        pages = PdfReader(f'{input_dir}/{prefix}{i+1}.pdf').pages
        outdata.addpage(pages[0])
        outdata.write()

    print("combine pdf done")

def rotate_pdf(file_path, rotate):
    if not os.path.exists(file_path):
        print(f"{file_path} does not exist")
        return

    assert rotate % 90 == 0

    output_path = os.path.dirname(file_path) + '/rotate_%s' % os.path.basename(file_path)

    trailer = PdfReader(file_path)
    pages = trailer.pages
  
    for pagenum in range(0, len(pages)):
        print(f"Rotate={pages[pagenum].inheritable.Rotate}")
        pages[pagenum].Rotate = (int(pages[pagenum].inheritable.Rotate or
                                    0) + rotate) % 360

    outdata = PdfWriter(output_path)
    outdata.trailer = trailer
    outdata.write()

    print(f'rotate_pdf, output_path={output_path}')
    return output_path

# 导出为新 pdf，version 1.4 -> 1.7
def export_new_file(file_path):
    if not os.path.exists(file_path):
        print(f"{file_path} does not exist")
        return

    result = fitz.open()

    for pdf in [file_path]:
        with fitz.open(pdf) as mfile:
            result.insert_pdf(mfile)

    new_file_name = 'new-' + os.path.basename(file_path)
    new_file_path = os.path.dirname(file_path) + '/' + new_file_name
        
    result.save(new_file_path)

    print(f"save as new file, new_file_path={new_file_path}")

    return new_file_path

# rotate_pdf('result.pdf', 180)
# combine_pdf_2('/Users/liusilan/documents/code-repo/py/pdf/result_82.pdf', '/Users/liusilan/documents/code-repo/py/pdf/rotate_result.pdf')

orginal_file_path1 = '/Users/liusilan/Downloads/pdf-test/image_t0000000082_n16.pdf'
orginal_file_path2 = '/Users/liusilan/Downloads/pdf-test/image_t0000000083_n16.pdf'
output_dir = '/Users/liusilan/Downloads/pdf-test'

# split_pdf(orginal_file_path1)
new_file_path1 = export_new_file(orginal_file_path1)
new_file_path2 = export_new_file(orginal_file_path2)

rotated_file_path2 = rotate_pdf(new_file_path2, 180)

# combine_pdf_2(new_file_path1, rotated_file_path2, output_dir)

