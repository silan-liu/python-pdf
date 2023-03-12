from audioop import reverse
from pypdf import PdfWriter, PdfReader, PdfMerger
import os
from datetime import datetime

# pip install pypdf, ptyhon 3.7+

def rotate_pdf(file_path, degree):
    if not os.path.exists(file_path):
        print(f"{file_path} does not exist")
        return

    assert degree % 90 == 0

    reader = PdfReader(file_path)
    writer = PdfWriter()

    pages = reader.pages
    for i in range(0, len(pages)):
        writer.add_page(pages[i])
        writer.pages[i].rotate(degree)

    output_path = os.path.dirname(file_path) + '/rotated_%s' % os.path.basename(file_path)

    with open(output_path, "wb") as fp:
        writer.write(fp)

    print("done")

def combine_pdf(file_path1, file_path2, output_dir = None):
    if not os.path.exists(file_path1) or not os.path.exists(file_path2):
        print("file path does not exist")
        return
    
    reader1 = PdfReader(open(file_path1, 'rb'))
    reader2 = PdfReader(open(file_path2, 'rb'))

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

    print(output_path)

    writer = PdfWriter()

    for i in range(0, len(pages1)):

        # 正序
        writer.add_page(pages1[i])

        # 倒序
        writer.add_page(pages2[len(pages2) - i - 1])

    output = open(output_path,'wb') 
    writer.write(output)
    output.close() 

    pass

def merge_pdf():

    merger = PdfMerger()

    # for pdf in ["file1.pdf", "file2.pdf", "file3.pdf"]:
    #     merger.append(pdf)

    input1 = open("/Users/liusilan/Downloads/pdf-test/image_t0000000082_n16.pdf", "rb")
    input2 = open("/Users/liusilan/Downloads/pdf-test/image_t0000000083_n16.pdf", "rb")
    input3 = open("combine_6_11.pdf", "rb")

    # merger.append("combine_0_5.pdf", (0,5))  # append the first 5 pages of source.pdf

    # add the first 3 pages of input1 document to output
    merger.append(fileobj=input2, pages=(0, 1))

    # insert the first page of input2 into the output beginning after the second page
    merger.merge(position=1, fileobj=input1)

    # append entire input3 document to the end of the output document
    merger.append("combine_6_11.pdf")

    # Write to an output PDF document
    output = open("document-output.pdf", "wb")
    merger.write(output)

    # Close File Descriptors
    merger.close()
    output.close()

def rename_file(dir_name):
    if not os.path.exists(dir_name):
        print(f"{dir_name} not exists")
        return

    for file in os.listdir(dir_name):
        if file.endswith('.pdf'):
            last_name = file.split('_')[-1]
            src_path = os.path.join(dir_name, file)
            dest_path = os.path.join(dir_name, last_name)

            print(f"last_name={last_name}, src_path={src_path}, dest_path={dest_path}")
            os.rename(src_path, dest_path)

    print(f"rename {dir_name} done")


# step = 2 递增虫命名，当 reverse = True 时，反序递增，即原文件名后的数字越大，新名字的数字越小，从 2 开始
def rename_files_with_step2(dir_name, reverse = False):
    if not os.path.exists(dir_name):
        print(f"{dir_name} not exists")
        return
    
    for file in os.listdir(dir_name):
        last_name = file.split('.')[0].split('_')[-1]
        new_file_name = str(int(last_name) * 2 - 1) + '.pdf'

        src_path = os.path.join(dir_name, file)
        dest_path = os.path.join(dir_name, new_file_name)
        os.rename(src_path, dest_path)

    if reverse:
        files = filter_files(dir_name, '.pdf')
        descend_files = sorted(files, key=lambda x: float(".".join(x.split('.')[0:-1])), reverse=True)
        print(descend_files)

        start = 2
        for file in descend_files:
            src_path = os.path.join(dir_name, file)

            new_file_name = f"{start}.pdf"
            start += 2

            dest_path = os.path.join(dir_name, new_file_name)
            os.rename(src_path, dest_path)


def filter_files(dir_name, extension):
    if not os.path.exists(dir_name):
        print(f"{dir_name1} not exists")
        return

    files = os.listdir(dir_name)
    filter_files = []
    for file in files:
        if file.endswith(extension):
            filter_files.append(file)

    return filter_files

def combine_files(dir_name1, dir_name2, output_dir=None):
    if not os.path.exists(dir_name1) or not os.path.exists(dir_name2):
        print(f"dir_name1 or dir_name2 not exists")
        return

    extension = '.pdf'

    # dir_name1 正序
    files1 = filter_files(dir_name1, extension)
    ascend_files = sorted(files1, key=lambda x: float(".".join(x.split('.')[0:-1])))
    print(f"ascend_files={ascend_files}")

    # dir_name2 倒序
    files2 = filter_files(dir_name2, extension)
    descend_files = sorted(files2, key=lambda x: float(".".join(x.split('.')[0:-1])), reverse=True)
    print(f"descend_files={descend_files}")

    if len(ascend_files) != len(descend_files):
        print("file count is not equal, please check it")
        return

    merger = PdfMerger()

    for i in range(len(ascend_files)):
        pdf1 = ascend_files[i]
        pdf2 = descend_files[i]

        pdf1_path = os.path.join(dir_name1, pdf1)
        pdf2_path = os.path.join(dir_name2, pdf2)

        print(f"pdf1_path={pdf1_path}, pdf2_path={pdf2_path}")

        merger.append(pdf1_path)
        merger.append(pdf2_path)


    if not output_dir:
        output_dir = os.path.dirname(file_path1)

    os.makedirs(output_dir, exist_ok=True)

    now = datetime.now()  # current date and time
    timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")

    output_path = f"{output_dir}/combined-output-{timestamp}.pdf"

    output = open(output_path, "wb")
    merger.write(output)

    # Close File Descriptors
    merger.close()
    output.close()

    print(f"combine pdf done, output_path = {output_path}")

def process_files(dir_name1, dir_name2, output_dir):
    # rename
    rename_file(dir_name1)
    rename_file(dir_name2)

    # combine
    combine_files(dir_name1, dir_name2, output_dir)

file_path1 = '/Users/liusilan/Documents/code-repo/py/pdf/result_82.pdf'
file_path2 = '/Users/liusilan/Documents/code-repo/py/pdf/result.pdf'

dir_name1 = '/Users/liusilan/Downloads/测试文件4/image_t0000000082_n16'
dir_name2 = '/Users/liusilan/Downloads/测试文件4/image_t0000000083_n16'
output_dir = '/Users/liusilan/Downloads/测试文件/output'

rotate_pdf('/Users/liusilan/Downloads/pdf-test/new-image_t0000000083_n16.pdf', 180)
# combine_pdf(file_path1, file_path2, output_dir)

# process_files(dir_name1, dir_name2, output_dir)

# 正序
# rename_files_with_step2(dir_name1, False)

# 反序
# rename_files_with_step2(dir_name2, True)







