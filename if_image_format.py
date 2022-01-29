import pandas as pd
import urllib.request
from PIL import Image

urllist_csv = input("input path of csv file")
urllist_df = pd.read_csv(urllist_csv, header=None)
urllist = urllist_df[0].values.tolist()

def url_to_img(url, idx):
    img = urllib.request.urlretrieve(url, "./{}.png".format(idx))
    return img

def crop_center(img, name):
    x, y = img.width, img.height
    sx = x // 2 - (min(x, y) // 2)
    sy = y // 2 - (min(x, y) // 2)
    img = img.crop((sx, sy, sx + min(x, y), sy + min(x, y)))

    return img.save('./{}.png'.format(name), 'png')

for url in enumerate(urllist):
    url_to_img(url[1], url[0])
    name = ('{}.png'.format(url[0]))
    img = Image.open('./{}'.format(name))
    crop_center(img, 'cropped_{}'.format(name))
    print('----{0}/{1} have saved!!----'.format(url[0] + 1, len(urllist)))