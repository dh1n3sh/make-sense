try:
    import os
    import sys
    import json
    from pdf2image import convert_from_path

    if sys.argv[1] == "-h" or sys.argv[1] == '-help':
        raise Exception()

    files = os.listdir(sys.argv[1])

    infodict = {"filesdone":["info.json"],"counter":0}

    if "info.json" in files: 
        with open(os.path.join(sys.argv[1],"info.json"),"r") as infofile:
            infodict = json.load(infofile)

    for singlefile in files:
        if singlefile not in infodict["filesdone"] :
            filecnt = infodict["counter"] + 1
            infodict["filesdone"].append(singlefile)
            pdf = convert_from_path(os.path.join(sys.argv[1],singlefile))
            cnt = 1
            for page in pdf:
                page.save(os.path.join(sys.argv[2],str(filecnt)+"_"+str(cnt)+".jpg"),"JPEG")
                cnt+=1
            infodict["counter"] = filecnt

    print("completed : ")
    print(infodict)
    with open(os.path.join(sys.argv[1],"info.json"),"w") as infofile:
        json.dump(infodict,infofile)
except :
    print("Usage :")
    print("python/python3 toImage.py <input_dir_path> <output_dir_path>")
    print("pre-requisite :")
    print("sudo apt install poppler-utils")
    print("pip/pip3 install pdf2image")
    # print("error : ")
    # print(sys.exc_info())