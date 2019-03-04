import glob
import os

import uuid

from PIL import Image
from data.account import session, Post, User

# 上传图片的保存路径
upload_pic_path = os.path.join('static', 'upload', '*.jpg')

# 略缩图保存路径
thumbnail_path = os.path.join('static', 'thumb', '*.jpg')


# 获取要展示的图片路径
def get_imgs():
    '''
    :return: 上传图片文件夹中所有图片的文件路径
    '''
    return glob.glob(upload_pic_path)


# 获取略缩图路径
def get_thumbnail():
    '''
    :return: 略缩图文件夹中所有图片的文件路径
    '''
    return glob.glob(thumbnail_path)


class UploadImage(object):
    """
    功能： 辅助保存用户上传图片，生成相关略缩图，记录相关URL
    """

    upload_dir = 'upload'
    thumb_dir = 'thumb'
    thumb_size = (200, 200)

    def __init__(self, old_name, static_path):
        """
        类初始化方法
        :param old_name:
        :param static_path:
        """
        self.old_name = old_name

        # 新的文件名将会是唯一的，不会重复的
        self.name = self.gen_new_name()
        self.static_path = static_path

    def gen_new_name(self):
        """
        生成唯一的文件ID，用来作为图片的名字
        :param old_name: 旧名字
        :return: 新生成的名字
        """
        _, ext = os.path.splitext(self.old_name)
        return uuid.uuid4().hex + ext

    @property
    def upload_url(self):
        """
        使用property是让该方法变成一个属性
        :return: 保存图片的相对路径的url
        """
        return os.path.join(self.upload_dir, self.name)

    @property
    def upload_path(self):
        """
        :return:upload_path
        """
        return os.path.join(self.static_path, self.upload_url)

    def save_upload_pic(self, content):
        """
        保存上传的文件
        :param image: 上传的reqest.file对象
        :return: 保存后的文件路径
        """
        with open(self.upload_path, 'wb') as fp:
            fp.write(content)

    @property
    def thumb_url(self):
        """
        生成用来保存图片缩略图相对路径的url
        :return:thum_url
        """
        name, ext = os.path.splitext(self.name)

        thumb_name = f'{self.thumb_size[0]}x{self.thumb_size[1]}_{name}'

        return os.path.join(self.thumb_dir, thumb_name)

    def save_thumbnail(self):
        """
        生成略缩图并保存，返回其路径
        :param image_path: 大图的图片路径
        :return: 生成的略缩图的文件路径
        """

        im = Image.open(self.upload_path)

        im.thumbnail(self.thumb_size)

        # 获取最后的xxx.jpg

        im.save(os.path.join(self.static_path, self.thumb_url))



def save_upload_pic(upload_img):
    """
    保存上传的大图片的函数
    :param image: 上传的reqest.file对象
    :return: 保存后的文件路径
    """

    # {"filename":..., "content_type":..., "body":...}
    # html content type对照表

    # save_pic_path = os.path.join('static/upload', upload_img['filename'])

    save_pic_path = f'static/upload/{upload_img["filename"]}'

    with open(save_pic_path, 'wb') as fp:
        fp.write(upload_img['body'])

    return save_pic_path


# 生成略缩图并保存，返回其路径
def save_thumbnail(image_path):
    """
    :param image_path: 大图的图片路径
    :return: 生成的略缩图的文件路径
    """

    im = Image.open(image_path)

    size = (200, 200)

    im.thumbnail(size)

    # 获取最后的xxx.jpg
    name = os.path.basename(image_path)

    thumb_path = f'static/thumb/{size[0]}x{size[1]}_{name}'

    im.save(thumb_path)

    return thumb_path


def add_post_for(telephone, image_url, thumb_url):
    """
    把用户上传图片的信息存入DB， 会生成一个post的数据对象
    :param telephone: 对应用户的telephone
    :param image_url: 上传图片的路径
    :param thumb_url: 略缩图路径
    :return: 该post对象
    """

    user = session.query(User).filter_by(telephone=telephone).first()

    post = Post(image_url=image_url, thumb_url=thumb_url, user=user)

    session.add(post)

    session.commit()

    return post


# 根据id取图片路径
def get_post_by_id(post_id):
    '''
    :param post_id: post的id值
    :return: 该post所有数据
    '''
    post = session.query(Post).filter_by(id=post_id).first()
    return post


# 获取所有post
def get_all_post():
    '''
    :return: 所有的post
    '''
    return session.query(Post).all()









if __name__ == '__main__':
    paths_01 = get_imgs()
    paths_02 = get_thumbnail()
    print(paths_01)
    print(paths_02)