import glob
from PIL import Image
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as T
import config as c

def to_rgb(image):
    rgb_image = Image.new("RGB", image.size)
    rgb_image.paste(image)
    return rgb_image

class Hinet_Dataset(Dataset):
    def __init__(self, transforms_=None, mode="train"):
        self.transform = transforms_
        self.mode = mode
        if mode == 'train':
            # train
            self.files_1 = sorted(glob.glob(c.TRAIN_PATH + "/cover/*." + c.format_train))
            self.files_2 = sorted(glob.glob(c.TRAIN_PATH + "/secret/*." + c.format_train))
            self.files = self.files_1 + self.files_2
            self.files = self.files[:500]
        else:
            # test
            self.files_1 = sorted(glob.glob(c.VAL_PATH + "/cover/*." + c.format_val))
            self.files_2 = sorted(glob.glob(c.VAL_PATH + "/secret/*." + c.format_val))
            self.files = self.files_1 + self.files_2
            self.files = self.files[:500]



    def __getitem__(self, index):
        try:
            img = Image.open(self.files[index])
            img = to_rgb(img)
            item = self.transform(img)
            return item

        except:
            return self.__getitem__(index + 1)

    def __len__(self):
        if self.mode == 'shuffle':
            return max(len(self.files_cover), len(self.files_secret))

        else:
            return len(self.files)
transform = T.Compose([
    T.RandomHorizontalFlip(),
    T.RandomVerticalFlip(),
    T.RandomCrop(c.cropsize),
    T.ToTensor()
])

transform_val = T.Compose([
    T.CenterCrop(c.cropsize_val),
    T.ToTensor(),
])


# Training data loader
# trainloader = DataLoader(
#     Hinet_Dataset(transforms_=transform, mode="train"),
#     batch_size=c.batch_size,
#     shuffle=True,
#     pin_memory=True,
# #    num_workers=8,
#     drop_last=True
# )
trainloader = DataLoader(
    Hinet_Dataset(transforms_=transform, mode="train"),
    batch_size=c.batch_size,
    shuffle=True,
    pin_memory=True,
    num_workers=8,
    drop_last=True
)
# Test data loader
testloader = DataLoader(
    Hinet_Dataset(transforms_=transform_val, mode="val"),
    batch_size=c.batchsize_val,
    shuffle=False,
    pin_memory=True,
    num_workers=1,
    drop_last=True
)
