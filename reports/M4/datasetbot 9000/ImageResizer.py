from PIL import Image
import os, sys
from subprocess import Popen



dir_path = "download"

def resize_im(path):
    if os.path.isfile(path):
        # dm = Image.open(path)
        # dm.save(os.path.join(parent_dir, img_name)+'.jpg', 'JPEG')
        im = Image.open(path).resize((100,100), Image.ANTIALIAS)
        parent_dir = os.path.dirname(path)
        img_name = os.path.basename(path).split('.')[0]
        im.save(os.path.join(parent_dir, img_name + '.jpg'), 'JPEG', quality=90)

def resize_all(mydir):
    for subdir , _ , fileList in os.walk(mydir):
        for f in fileList:
            try:
                full_path = os.path.join(subdir,f)
                resize_im(full_path)
            except Exception as e:
                try:
                    os.remove(full_path)
                    print('Unable to resize %s.Hence deleted' % full_path)
                except Exception as e:
                    print("Important! undeleteable unrecognised file found: %s" % full_path)


def bat():
    p = Popen("rename.bat")
    stdout, stderr = p.communicate()

if __name__ == '__main__':
    bat()
    resize_all(dir_path)