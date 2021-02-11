from pathlib import Path, PurePath
import datetime
import shutil
import logging

log_path = Path("../log/")
if not log_path.exists():
    log_path.mkdir()
logging.basicConfig(format='%(asctime)s %(message)s', level = logging.WARNING, filename = Path(log_path,"log.txt"))


#put this in a config file later?
photo_path = "photo"
video_path = "video"
img_ext = ['.CR2','.jpg','.jpeg','.png','.tif','.tiff','.tga','.bmp','.exr','.hdr']
vid_ext = ['.mp4','.mov','.MOV','.m4v','.avi', '3gp']
in_path = Path('//LURCH/homeshare/media/in/').glob('**/*')
start_path = Path('//LURCH/homeshare/media/')

#fetch files in the folder
files = [f for f in in_path if f.is_file()]
#print(files)

#init file list
filelist = []

for f in files:
    ctime = datetime.datetime.fromtimestamp(f.stat().st_ctime)
    fileinfo = [f.name, f.suffix, f, ctime]
    filelist.append(fileinfo)

def getMediaType(ext):
    if ext in img_ext:
        return photo_path
    if ext in vid_ext:
        return video_path

for f in filelist:
    #start counter
    sumfiles = 0
    #more usefull names for whats in the list
    filename = f[0]
    fileext = f[1]
    filepath = f[2]
    createtime = f[3]
    #check if Extension is allowed
    if getMediaType(fileext) is not None:
        path_to_create = Path(start_path,  getMediaType(fileext) , str(createtime.year) , str(createtime.month))
        #check if dir exists else create
        if not path_to_create.is_dir():
            path_to_create.mkdir(parents=True)
        #define source and target
        source = filepath
        target = Path(path_to_create, filename)

        if not target.exists():
            shutil.copyfile(source, target)
            logging.info(f"Copied {source} to {target}")
            sumfiles+=1
            #check if succes, if so delete
            if target.exists():
                logging.info(f"Removed {source}")
                source.unlink()
        ##add extra option here to check filesize if the same exact size then skip else, rename and copy
        else:
            logging.warning(f"File {target} exists, skipping...")
    else:
        logging.warning(f"Extension {fileext} of {filename} not recognized!, skipping...")

logging.info(f"FINISHED! - Copied {sumfiles}")
