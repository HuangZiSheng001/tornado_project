import glob
import os

import uuid

from PIL import Image
from sqlalchemy_pagination import paginate

from data.account import session, Post, User, Like

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

        self.uuid_name = self.gen_uuid_name()
        self.ext = self.get_ext(old_name)

        # 拼凑起来的完整文件名
        self.name = self.uuid_name + self.ext
        self.static_path = static_path

    def get_ext(self, old_name):
        """
        获取后缀
        :return: 获取后缀
        """
        _, ext = os.path.splitext(old_name)
        return ext

    def gen_uuid_name(self):
        """
        生成唯一的文件ID，用来作为图片的名字
        :return:唯一的文件id
        """
        return uuid.uuid4().hex

    @property
    def upload_img_url(self):
        """
        使用property是让该方法变成一个属性
        生成保存图片的相对路径的url
        :return: 保存图片的相对路径的url
        """
        return os.path.join(self.upload_dir, self.name)

    @property
    def upload_path(self):
        """
        :return:upload_path
        """
        return os.path.join(self.static_path, self.upload_img_url)

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
        :return:thum_url   保存图片缩略图相对路径的url
        """
        thumb_name = '{}x{}_{}{}'.format(
            self.thumb_size[0],
            self.thumb_size[1],
            self.uuid_name,
            self.ext,
        )

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


class OrmHandler(object):
    """
    SQL ORM 管理   每次打开session操作完就关闭，保障各个进程之间能正产访问session
    """

    def __init__(self, db_session, user_phone):
        """
        :param db_session:
        :param user_phone: self.current_user  为用户的号码
        """
        self.db_session = db_session
        self.user_telephone = user_phone
        
    def get_user(self):
        user = self.db_session.query(User).filter(User.telephone == self.user_telephone).first()
        return user

    def add_post_for(self, image_url, thumb_url):
        """
        把用户上传图片的信息存入DB， 会生成一个post的数据对象
        :param telephone: 对应用户的telephone
        :param image_url: 上传图片的路径
        :param thumb_url: 略缩图路径
        :return: 该post对象
        """

        user = self.db_session.query(User).filter_by(telephone=self.user_telephone).first()

        post = Post(image_url=image_url, thumb_url=thumb_url, user=user)

        self.db_session.add(post)

        self.db_session.commit()

        return post

    def get_post_by_id(self, post_id):
        """
        根据id取图片路径
        :param post_id: post的id值
        :return: 该post所有数据
        """
        post = self.db_session.query(Post).filter_by(id=post_id).first()
        return post

    def get_all_post(self, page):
        """
        获取所有post
        :return: 所有的post
        """
        posts = self.db_session.query(Post).order_by(Post.id.desc())
        pg = paginate(query=posts, page=page, page_size=10)
        return pg.items

    def get_posts_for(self):
        """
        :param user_phone: 某一用户的所有post
        :return: 该用户拥有（上传）的所有post数据
        """
        user = self.db_session.query(User).filter_by(telephone=self.user_telephone).first()
        if user:
            return self.db_session.query(Post).filter_by(user_id=user.id).order_by(Post.id.desc()).all()
        else:
            return []

    def get_like_posts(self):
        """
        获取该用户喜爱的图片
        :param telephone:
        :return: 该用户收藏的所有post的id
        """
        user = self.db_session.query(User).filter(User.telephone == self.user_telephone).first()
        if user:
            return self.db_session.query(Post). \
                filter(Like.post_id == Post.id, Like.user_id == user.id) \
                .order_by(Post.id.desc()).all()
        else:
            return []

    def make_page(self, page, per_page=10):
        """
        分页的函数
        :param page:
        :param per_page:
        :return:
        """
        posts = self.db_session.query(Post).order_by(Post.id.desc())
        pg = paginate(query=posts, page=page, page_size=per_page)
        return pg

    def get_like_count(self, post_id):
        """
        统计该post(的图片)喜欢的人数
        :param post_id:
        :return:
        """
        return self.db_session.query(User).filter(User.id == Like.user_id, Like.post_id == post_id).count()

    def mark_like(self, post_id):
        """
        当前用户 收藏 该图片的动作
        :param post_id:
        :param username:
        :return:
        """
        user = self.db_session.query(User).filter_by()
        pass

    def is_like(self, current_user_telephone, post):
        """
        判断当前用户是否喜欢了该图片
        :return:
        """
        pass


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


def get_post_by_id(post_id):
    """
    根据id取图片路径
    :param post_id: post的id值
    :return: 该post所有数据
    """
    post = session.query(Post).filter_by(id=post_id).first()
    return post


def get_all_post(page):
    """
    获取所有post
    :return: 所有的post
    """
    posts = session.query(Post).order_by(Post.id.desc())
    pg = paginate(query=posts, page=page, page_size=10)
    return pg.items


def get_posts_for(user_phone):
    """
    :param user_phone: 某一用户的所有post
    :return: 该用户拥有（上传）的所有post数据
    """
    user = session.query(User).filter_by(telephone=user_phone).first()
    if user:
        return session.query(Post).filter_by(user_id=user.id).order_by(Post.id.desc()).all()
    else:
        return []


def get_like_posts(telephone):
    """
    获取该用户喜爱的图片
    :param telephone:
    :return: 该用户收藏的所有post的id
    """
    user = session.query(User).filter(User.telephone == telephone).first()
    if user:
        return session.query(Post).\
            filter(Like.post_id == Post.id, Like.user_id == user.id)\
            .order_by(Post.id.desc()).all()
    else:
        return []


def make_page(page, per_page=10):
    """
    分页的函数
    :param page:
    :param per_page:
    :return:
    """
    posts = session.query(Post).order_by(Post.id.desc())
    pg = paginate(query=posts, page=page, page_size=per_page)
    return pg


def get_like_count(post_id):
    """
    统计该post(的图片)喜欢的人数
    :param post_id:
    :return:
    """
    return session.query(User).filter(User.id == Like.user_id, Like.post_id == post_id).count()


def mark_like(post_id, telephone):
    """
    当前用户 收藏 该图片的动作
    :param post_id:
    :param username:
    :return:
    """
    user = session.query(User).filter_by()


def is_like(current_user_telephone, post):
    """
    判断当前用户是否喜欢了该图片
    :return:
    """
    pass






def save_upload_pic(upload_img):
    """
    保存上传的大图片的函数
    :param image: 上传的reqest.file对象
    :return: 保存后的文件路径
    """

    # {"filename":..., "content_type":..., "body":...}
    # html content type对照表

    # save_pic_path = os.path.join('static/upload', upload_img['filename'])

    save_pic_path = 'static/upload/{}'.format(
        upload_img["filename"],
    )

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

    thumb_path = 'static/thumb/{}x{}_{}'.format(
        size[0],
        size[1],
        name,
    )

    im.save(thumb_path)

    return thumb_path






if __name__ == '__main__':
    paths_01 = get_imgs()
    paths_02 = get_thumbnail()
    print(paths_01)
    print(paths_02)