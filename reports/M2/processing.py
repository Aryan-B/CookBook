import os

with open('classes.txt', 'w+') as f:
    f.write('\n'.join(os.listdir('train')))

for idx, i in enumerate(os.listdir('train')):
    os.rename('train\{}'.format(i), 'train\{}'.format(idx))
    os.rename('test\{}'.format(i), 'test\{}'.format(idx))