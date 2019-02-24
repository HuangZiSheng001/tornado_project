import glob
import os
from PIL import Image

# 上传图片的保存路径
upload_pic_path = os.path.join('static', 'upload', '*.jpg')

# 略缩图保存路径
thumbnail_path = os.path.join('static', 'thumb', '*.jpg')


# 获取要展示的图片路径
def get_imgs():
    return glob.glob(upload_pic_path)

# 获取略缩图路径
def get_thumbnail():
    return glob.glob(thumbnail_path)


# 生成略缩图并转换
def save_thumbnail(image_path):
    im = Image.open(image_path)
    size = (200, 200)

    im.thumbnail(size)
    name = os.path.basename(image_path)

    im.save('static/thumb/{}x{}_{}'.format(
            size[0],
            size[1],
            name,
        )
    )


if __name__ == '__main__':
    paths_01 = get_imgs()
    paths_02 = get_thumbnail()
    print(paths_01)
    print(paths_02)