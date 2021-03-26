import os, shutil

begin_path = 'b'
end_path = 'c'

idx = 0
for i in os.listdir(begin_path):
    shutil.copy(os.path.join(begin_path, i), os.path.join(end_path, '{}.jpg'.format(idx)))
    idx += 1