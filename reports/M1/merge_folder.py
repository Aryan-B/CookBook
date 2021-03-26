import os, shutil

begin_path = 'a'
end_path = 'b'

idx = 0
for i in os.listdir(begin_path):
    base_path = os.path.join(begin_path, i)
    for j in os.listdir(base_path):
        shutil.copy(os.path.join(base_path, j), os.path.join(end_path, '{}.jpg'.format(idx)))
        # shutil.copy(os.path.join(base_path, j), os.path.join(end_path, j))
        idx += 1