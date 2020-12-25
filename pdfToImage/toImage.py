import argparse
import json
import os
import sys

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

    parser = argparse.ArgumentParser(
        description="Convert a directory of pdfs into images.")
    parser.add_argument('input_dir', type=str,
                        help="Relative path to the input directory which contains the pdfs.")
    parser.add_argument('output_dir', type=str,
                        help="Relative path to the output directory to store the images.")

    args = parser.parse_args()
    ip_dir = args.input_dir
    op_dir = args.output_dir
    status = convert_pdfs_to_images(ip_dir, op_dir)
    print("completed : ")
    print(json.dumps(status, indent=2))
