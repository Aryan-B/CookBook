import matplotlib.pyplot as plt
import numpy as np

with open('train.log') as f:
    mobilenetv2 = [i for i in list(map(lambda x:x.strip(), f.readlines())) if 'epoch' in i]

mobilenetv2 = [i.split(',') for i in mobilenetv2]
mobilenetv2 = np.array([np.array(list(map(lambda x:float(x.split(':')[1]), i[2:]))) for i in mobilenetv2])

plt.subplot(2, 2, 1)
plt.plot(list(range(len(mobilenetv2))), mobilenetv2[:, 0])
plt.title('loss')
plt.xlabel('epoch')
plt.legend()

plt.subplot(2, 2, 2)
plt.plot(list(range(len(mobilenetv2))), mobilenetv2[:, 1])
plt.title('val_loss')
plt.xlabel('epoch')
plt.legend()

plt.subplot(2, 2, 3)
plt.plot(list(range(len(mobilenetv2))), mobilenetv2[:, 2])
plt.title('acc')
plt.xlabel('epoch')
plt.legend()

plt.subplot(2, 2, 4)
plt.plot(list(range(len(mobilenetv2))), mobilenetv2[:, 3])
plt.title('val_acc')
plt.xlabel('epoch')
plt.legend()

plt.show()