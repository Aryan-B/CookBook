import numpy as np

import torchvision.models as models
import torch, time, datetime, tqdm
import torch.nn as nn
from dataset import DataGenerator

BATCH_SIZE = 32
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(DEVICE)

model = models.mobilenet_v2(pretrained=True)
model.classifier = nn.Sequential(
    nn.Dropout(p=0.2, inplace=True),
    nn.Linear(in_features=1280, out_features=85, bias=True),
)

model = model.to(DEVICE)

train_generator = DataGenerator('train', batch_size=BATCH_SIZE)
valid_generator = DataGenerator('test', valid=True, batch_size=BATCH_SIZE)

# optimizer Adam
optimizer = torch.optim.Adam(params=model.parameters(), lr=0.0005, weight_decay=0.001)
lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.9)

# loss 
loss = torch.nn.CrossEntropyLoss()

best_acc = 0
print('{} begin train!'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
with open('train.log', 'w+') as f:
    for epoch in range(100):
        model.to(DEVICE)
        model.train()
        train_loss = 0
        correct = 0
        begin = time.time()
        num = 0
        for x, y in train_generator:
            x, y = x.to(DEVICE), y.to(DEVICE).long()

            pred = model(x.float())
            l = loss(pred, y)
            optimizer.zero_grad()
            l.backward()
            optimizer.step()

            y_pred = torch.max(pred.data, 1)
            correct += (y_pred.indices == y).sum().to('cpu').item()

            train_loss += float(l.data)
            num += 1

            if num == len(train_generator):
                break
        train_loss /= num
        train_acc = (correct / (num * BATCH_SIZE))
        lr_scheduler.step()

        num = 0
        test_loss = 0
        correct = 0
        model.eval()
        with torch.no_grad():
            for x, y in valid_generator:
                x, y = x.to(DEVICE), y.to(DEVICE).long()

                pred = model(x.float())
                l = loss(pred, y)
                num += 1
                test_loss += float(l.data)

                y_pred = torch.max(pred.data, 1)
                correct += (y_pred.indices == y).sum().to('cpu').item()

                if num == len(valid_generator):
                    break
        test_loss /= num
        test_acc = (correct / (num * BATCH_SIZE))

        if test_acc > best_acc:
            best_acc = test_acc
            model.to('cpu')
            torch.save(model, 'model.pht')
            print('{} save best_val_acc model success!'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        f.write(
            '{} epoch:{}, time:{:.2f}s, train_loss:{:.5f}, val_loss:{:.5f}, train_acc:{:.4f}, val_acc:{:.4f}\n'.format(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                epoch + 1, time.time() - begin, train_loss, test_loss, train_acc, test_acc
            ))
        print('{} epoch:{}, time:{:.2f}s, train_loss:{:.5f}, val_loss:{:.5f}, train_acc:{:.4f}, val_acc:{:.4f}'.format(
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            epoch + 1, time.time() - begin, train_loss, test_loss, train_acc, test_acc
        ))
        model.to('cpu')
        torch.save(model, 'model_{}.pht'.format(epoch))
