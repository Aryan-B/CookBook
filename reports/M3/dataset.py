import cv2, os, math, random, torch
import numpy as np
from torch.utils.data import Dataset

class DataGenerator(Dataset):
    def __init__(self, imgPath, batch_size=16, target_size=(224, 224), shuffle=True, valid=False):
        self.imgPath_list, self.classes = [], []

        for i in sorted(os.listdir(imgPath), key=lambda x: int(x)):
            base_path = os.path.join(imgPath, i)
            for j in os.listdir(base_path):
                self.imgPath_list.append(os.path.join(base_path, j))
                self.classes.append(int(i))
        self.classes = self.classes
        self.imgPath_list, self.classes = np.array(self.imgPath_list), np.array(self.classes)
        self.batch_size = batch_size
        self.target_size = target_size
        self.shuffle = shuffle
        self.valid = valid
        self.indexes = np.arange(len(self.imgPath_list))
        np.random.shuffle(self.indexes)

    def __len__(self):
        return int(np.floor(len(self.imgPath_list) / self.batch_size))

    def __getitem__(self, index):
        if index == 0:
            np.random.shuffle(self.indexes)

        indexes = self.indexes[index * self.batch_size:(index + 1) * self.batch_size]

        x, y = [], []
        for i, j in zip(self.imgPath_list[indexes], self.classes[indexes]):
            x.append(self.__data_generation(i))
            y.append(j)

        x, y = np.array(x, dtype=np.float) / 255.0, np.array(y)
        x = np.transpose(x, (0, 3, 1, 2))

        x, y = torch.from_numpy(x), torch.from_numpy(y)

        return x, y

    def __data_generation(self, img_path):
        random_int = random.randint(1, 16)
        if self.valid:
            random_int = 9

        img = cv2.imdecode(np.fromfile(img_path, np.uint8), cv2.IMREAD_COLOR)
        if random_int == 1:
            img = self.random_crop(img)
        elif random_int == 2:
            img = self.rule_crop(img)
        elif random_int == 3:
            img = self.flip(img)
        elif random_int == 4:
            img = self.random_noise(img)
        elif random_int == 5:
            img = self.equalize_hist(img)
        elif random_int == 6:
            img = self.rotate(img)
        elif random_int == 7:
            img = self.adjust_contrast_bright(img)
        elif random_int == 8:
            img = self.random_USM(img)
        else:
            pass

        img = cv2.resize(img, (224, 224))
        return img

    def random_crop(self, img, scale=[0.8, 1.0], ratio=[3. / 4., 4. / 3.]):
        """
        Random clipping
        """
        aspect_ratio = math.sqrt(np.random.uniform(*ratio))
        w = 1. * aspect_ratio
        h = 1. / aspect_ratio
        src_h, src_w = img.shape[:2]

        bound = min((float(src_w) / src_h) / (w ** 2),
                    (float(src_h) / src_w) / (h ** 2))
        scale_max = min(scale[1], bound)
        scale_min = min(scale[0], bound)

        target_area = src_h * src_w * np.random.uniform(scale_min, scale_max)
        target_size = math.sqrt(target_area)
        w = int(target_size * w)
        h = int(target_size * h)

        i = np.random.randint(0, src_w - w + 1)
        j = np.random.randint(0, src_h - h + 1)

        img = img[j:j + h, i:i + w]
        img = cv2.resize(img, (self.target_size))
        return img

    def rule_crop(self, img, box_ratio=(3. / 4, 3. / 4), location_type='LT'):
        """
        Cut according to certain rules, 
        operate directly on the size of the original image, 
        not the original image
        :param img:
        :param box_ratio: cutting ratio:  (ratio in width, ratio in height)
        :param location_type: Specific location: one of the following:
                LT : top left
                RT : top right
                LB : bottem left
                RB : bottem right
                CC : center
        :param resize_w: output's width
        :param resize_h: output's height
        :return:
        """
        assert location_type in ('LT', 'RT', 'LB', 'RB', 'CC'), 'must have a location .'
        is_gray = False
        if len(img.shape) == 3:
            h, w, c = img.shape
        elif len(img.shape) == 2:
            h, w = img.shape
            is_gray = True

        crop_w, crop_h = int(w * box_ratio[0]), int(h * box_ratio[1])
        crop_img = np.zeros([10, 10])
        if location_type == 'LT':
            crop_img = img[:crop_h, :crop_w, :] if not is_gray else img[:crop_h, :crop_w]
        elif location_type == 'RT':
            crop_img = img[:crop_h:, w - crop_w:, :] if not is_gray else img[:crop_h:, w - crop_w:]
        elif location_type == 'LB':
            crop_img = img[h - crop_h:, :crop_w, :] if not is_gray else img[h - crop_h:, :crop_w]
        elif location_type == 'RB':
            crop_img = img[h - crop_h:, w - crop_w:, :] if not is_gray else img[h - crop_h:, w - crop_w:]
        elif location_type == 'CC':
            start_h = (h - crop_h) // 2
            start_w = (w - crop_w) // 2
            crop_img = img[start_h:start_h + crop_h, start_w:start_w + crop_w, :] if not is_gray else img[start_h:start_h + crop_h,start_w:start_w + crop_w]

        resize = cv2.resize(crop_img, (self.target_size))
        return resize

    def flip(self, img):
        """
        flip
        :param img:
        :param mode: 1=flip horizontal / 0=vertical / -1=pan/shift
        :return:
        """
        mode = np.random.choice([-1, 0, 1])
        return cv2.flip(img, flipCode=mode)

    def random_USM(self, img, gamma=0.):
        """
        The sharpening algorithm of USM can remove some small interfering details and image noise, 
        which is more reliable than the image obtained by using the convolution sharpening operator directly.
            output = Original image −w∗ Gaussian filter (Original image)/(1−w)
            w's range is 0.1~0.9，usually use 0.6
        :param img:
        :param gamma:
        :return:
        """
        blur = cv2.GaussianBlur(img, (0, 0), 25)
        img_sharp = cv2.addWeighted(img, 1.5, blur, -0.3, gamma)
        return img_sharp

    def random_noise(self, img, rand_range=(3, 20)):
        """
        random noise
        :param img:
        :param rand_range: (min, max)
        :return:
        """
        img = np.asarray(img, np.float)
        sigma = random.randint(*rand_range)
        nosie = np.random.normal(0, sigma, size=img.shape)
        img += nosie
        img = np.uint8(np.clip(img, 0, 255))
        return img

    def equalize_hist(self, img):
        """
        Histogram Equalization
        :param img:
        :return:
        """
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hist = cv2.equalizeHist(gray)
        rgb = cv2.cvtColor(hist, cv2.COLOR_GRAY2BGR)
        return rgb

    def rotate(self, img, angle=30, scale=1.0):
        """
        Rotate
        :param img:
        :param angle: rotation angle， >0 represents counterclockwise，
        :param scale:
        :return:
        """
        height, width = img.shape[:2]  # Gets the height and width of the image
        center = (width / 2, height / 2)  # Take the midpoint 
        angle = np.random.choice(np.arange(-angle, angle))

        M = cv2.getRotationMatrix2D(center, angle, scale)  
        # Obtain the rotation matrix of the image about a certain point
        # cv2.warpAffine() The second parameter is the transformation matrix, 
        # and the third parameter is the size of the output image
        rotated = cv2.warpAffine(img, M, (height, width))
        return rotated

    def adjust_contrast_bright(self, img, contrast=1.2, brightness=100):
        """
        Adjust brightness and contrast
        dst = img * contrast + brightness
        :param img:
        :param contrast: contrast   the larger the contrase, the brighter the images
        :param brightness: range  0~100
        :return:
        """
        # Pixel values can go beyond 0-255, so truncation is required
        return np.uint8(np.clip((contrast * img + brightness), 0, 255))