import os
import sys
import json
from pdf2image import convert_from_path


def convert_pdfs_to_images(ip_dir, op_dir):
    '''
    params
        ip_dir : The input directory which contains the pdfs.
        op_dir : The output directory to store the images.

    returns
        infodict : The status of pdfs converted.
    '''

    files = os.listdir(ip_dir)
    infodict = {"filesdone": [], "counter": 0}

    if "info.json" in files:
        with open(os.path.join(ip_dir, "info.json"), "r") as infofile:
            infodict = json.load(infofile)

    for singlefile in files:
        if singlefile not in infodict["filesdone"] and singlefile.endswith('.pdf'):
            filecnt = infodict["counter"] + 1
            infodict["filesdone"].append(singlefile)
            pdf = convert_from_path(os.path.join(ip_dir, singlefile))
            cnt = 1
            for page in pdf:
                page.save(os.path.join(sys.argv[2], str(
                    filecnt)+"_"+str(cnt)+".jpg"), "JPEG")
                cnt += 1
            infodict["counter"] = filecnt

    with open(os.path.join(ip_dir, "info.json"), "w") as infofile:
        json.dump(infodict, infofile)

    return infodict


if __name__ == '__main__':

    try:
        if sys.argv[1] == "-h" or sys.argv[1] == '-help':
            raise Exception()
        ip_dir = sys.argv[1]
        op_dir = sys.argv[2]
        status = convert_pdfs_to_images(ip_dir, op_dir)
        print("completed : ")
        print(json.dumps(status, indent=2))

    except:
        print("Usage :")
        print("python/python3 toImage.py <input_dir_path> <output_dir_path>")
        print("pre-requisite :")
        print("sudo apt install poppler-utils")
        print("pip/pip3 install pdf2image")
        # print("error : ")
        # print(sys.exc_info())
