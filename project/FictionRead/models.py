from django.db import models
'''
用户：用户基础信息放在t_user,隐私信息放在t_pri,订阅信息放在t_user_sub
作品：整本和章节均视为作品。作品信息放在t_art。特别的，整本的互动信息放在t_book。必须先添加作品再添加作品整本
用户与作品：点赞信息放在t_like,收藏信息放在t_coll,创作信息放在t_cre。
评论：t_con表
'''
class t_user(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32,unique=True)
    nickname = models.CharField(max_length=32,unique=True,null=True)
    pwd = models.CharField(max_length=32)
    email = models.CharField(max_length=255,null=True)
    phone = models.IntegerField(null=True)
    # MEDIA_ROOT 设置为项目根目录/media/
    avatar = models.FileField(upload_to='avatar/', default="/avatar/default.png")
    Intro = models.CharField(max_length=255,default='')
    register_time = models.DateTimeField(auto_now_add=True)
    last_login_time = models.DateTimeField(auto_now_add=True)

class t_user_sub(models.Model):
    # 用户1订阅了用户2
    user_1 =models.ForeignKey(t_user,on_delete=models.DO_NOTHING,related_name='u1')
    user_2 =models.ForeignKey(t_user,on_delete=models.DO_NOTHING,related_name='u2')

class t_art(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32,null=False)
    content = models.TextField(max_length=65535)
    index = models.IntegerField()
    book_id = models.IntegerField(null=True)
    pub_time = models.DateTimeField(auto_now_add=True)
    com_num = models.IntegerField()

class t_book(models.Model):
    art_id = models.ForeignKey(t_art,on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=32)
    # MEDIA_ROOT 设置为项目根目录/media/
    pic = models.FileField(upload_to='book/', default="book/default.png")
    coll_num = models.IntegerField()
    like_num = models.IntegerField()
    type = models.CharField(max_length=32)

class t_like(models.Model):
    user = models.ForeignKey(t_user,on_delete=models.DO_NOTHING)
    book = models.ForeignKey(t_book,on_delete=models.DO_NOTHING)

class t_coll(models.Model):
    user = models.ForeignKey(t_user,on_delete=models.DO_NOTHING)
    book = models.ForeignKey(t_book,on_delete=models.DO_NOTHING)

class t_cre(models.Model):
    user = models.ForeignKey(t_user,on_delete=models.DO_NOTHING)
    art = models.ForeignKey(t_art,on_delete=models.DO_NOTHING)

class t_pri(models.Model):
    user = models.ForeignKey(t_user, on_delete=models.DO_NOTHING)
    is_show_info = models.BooleanField(default=True)
    is_show_coll = models.BooleanField(default=True)
    is_show_like = models.BooleanField(default=True)
    is_show_sub = models.BooleanField(default=True)

class t_com(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(t_user, on_delete=models.DO_NOTHING,related_name='commenter')
    pub_time = models.DateTimeField(auto_now_add=True)
    anc_com = models.IntegerField(null=True)
    art = models.ForeignKey(t_art,on_delete=models.DO_NOTHING)
    rep_user = models.IntegerField(null=True)
    content = models.CharField(max_length=255,null=False)
    like_num = models.IntegerField()

class t_register_cache(models.Model):
    name = models.CharField(max_length=32,)
    pwd = models.CharField(max_length=32)
    email = models.CharField(max_length=255, null=True)
    random = models.CharField(max_length=255, unique=True)
