from django.shortcuts import render
# 引入发送邮件的模块
from django.core.mail import send_mail, send_mass_mail, EmailMultiAlternatives
from django.conf import settings
# Create your views here.
from django.http import HttpResponse

from .models import *
# 引入事务
from django.db import transaction

#发送验证码到指定邮箱
def vctoemail(email,vc):
    str = '注册成功！请到点击以下网址激活账号！\n'
    str += settings.index_path+'#'+vc
    res = send_mail('欢迎注册 --悦享小说网站',
              str,
              'fictionemail123@163.com',
              [email],
                fail_silently = False)
    # 值1：邮件标题   值2：邮件主人  值3：发件人  值4：收件人  值5：如果失败，是否抛出错误
    if res == 1:
        return HttpResponse('邮件发送成功')
    else:
        return HttpResponse('邮件发送失败')


import json


def userstation(request):
    response = None
    if request.method == 'GET':
        is_login = 0
        id = 0
        avatar = ''
        user_name = request.session.get('user_name', '')
        # print(user_name)
        if user_name:
            is_login = 1
            id = request.session['user_id']
            avatar = request.session['avatar']
        s = {
            'is_login': is_login,
            'user_id': id,
            'avatar': avatar,
            "unp_interaction": {

            },
        }

        response = HttpResponse(json.dumps(s), content_type="application/json")
        # response["Access-Control-Allow-Origin"] = "*"
        # response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        # response["Access-Control-Max-Age"] = "1000"
        return response
    else:
        return HttpResponse('只接受get请求')

import datetime
def login(request):
    if request.method == 'POST':
        user_name = request.session.get('user_name', '')
        user_password = None
        user_id = request.session.get('user_id', '')
        avatar = request.session.get('avatar', '')
        # 判断session是否有user_name
        is_login = 0
        msg = ""
        if not user_name:
            if request.POST.get('user_name'):
                user_name = request.POST['user_name']
            if request.POST.get('user_password'):
                user_password = request.POST['user_password']
            if user_name is not None and user_password is not None:
                # 在数据库中搜索
                user = t_user.objects.filter(name=user_name,pwd=user_password)
                if not user:
                    user = t_user.objects.filter(email=user_name, pwd=user_password)
                if user:
                    user = user[0]
                    user_name = user.name
                    # 更新登录时间
                    user.last_login_time = datetime.datetime.now()
                    # session存入user_name
                    request.session['user_name'] = user.name
                    request.session['avatar'] = str(user.avatar)
                    request.session['user_id'] = user.id
                    is_login = 1
                    msg = '登录成功！'
                else:
                    msg = '登录失败！'
        else:
            msg = '您已登录！'


        s = {
            'is_login': is_login,
            'user_name': user_name,
            'user_id': user_id,
            'avatar': avatar,
            "unp_interaction": {

            },
            'msg': msg
        }

        response = HttpResponse(json.dumps(s), content_type="application/json")
        # response["Access-Control-Allow-Origin"] = "*"
        # response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        # response["Access-Control-Max-Age"] = "1000"
        return response

    else:
        return HttpResponse('只接受Post请求')

def logout(request):
    request.session.flush()
    return HttpResponse('成功退出！')

import random,string

def register(request):
    if request.method == 'POST':
        user_name = ''
        user_password = ''
        email = ''
        is_register = 1
        if request.POST.get('user_name'):
            user_name = request.POST['user_name']
        if request.POST.get('user_password'):
            user_password = request.POST['user_password']
        if request.POST.get('email'):
            email = request.POST['email']
        # 再次验证用户表没有user_name，email，否则返回注册失败
        if(t_user.objects.filter(name=user_name) or t_user.objects.filter(email=email)):
            is_register = 0
        else:
            # 生成验证码
            num = string.ascii_letters + string.digits
            vc = ''.join(random.sample(num, 10))
            try:
                # 开启事务
                with transaction.atomic():
                    # 刷新验证码表
                    t_register_cache.objects.filter(name=user_name).delete()
                    t_register_cache.objects.filter(email=email).delete()
                    cache = t_register_cache(name=user_name, email=email,pwd=user_password ,random=vc)
                    cache.save()
                    # 发送邮件,其实应该再验证一遍email
                    vctoemail(email,vc)
            except Exception as e:
                return HttpResponse("数据库更新错误<%s>" % str(e))


            # 如果有的话，将t_10中用户名为user_name的删除
            # 生成随机码，发邮件到email,将随机码、时间等放入t_10

        # 返回注册成功信息
        s = {
            'is_register': is_register,
            'msg': '注册成功！'
        }

        response = HttpResponse(json.dumps(s), content_type="application/json")
        return response

    else:
        return HttpResponse('只接受Post请求')


def verification(request):
    if request.method == 'GET':
        vc = 0
        if (request.GET.get('vc')):
            vc = request.GET['vc']
        is_success = 0
        msg = ''
        id = ''
        # 查数据库
        cache_set = t_register_cache.objects.filter(random=vc)
        cache = None
        if cache_set:
            cache = cache_set[0]
        if cache:
            user = None
            try:
                # 开启事务
                with transaction.atomic():
                    # 更新t_user数据
                    user = t_user(name=cache.name,pwd=cache.pwd,email=cache.email)
                    user.save()
                    # 刷新验证码表
                    t_register_cache.objects.filter(name=user.name).delete()
                    is_success = 1
            except Exception as e:
                return HttpResponse("数据库更新错误<%s>" % str(e))
            # 查出自动生成的用户id数据
            if user:
                request.session['user_name'] = user.name
                request.session['avatar'] = str(user.avatar)
                id = user.id
                request.session['user_id'] = id
                msg = '恭喜！注册成功！您的ID为' + str(id)
        s = {
            'is_success': is_success,
            'msg': msg
        }
        # 其他处理
        # 将这个人的session里改成已登录状态
        response = HttpResponse(json.dumps(s), content_type="application/json")
        return response

    else:
        return HttpResponse('只接受GET请求')

# 注册时获取个人信息，判断用户是否存在
def userinfo(request):
    if request.method == 'GET':
        user = None
        # print(request.GET)
        if (request.GET.get('id')):
            id = request.GET['id']
            # 查找ID
            users = t_user.objects.filter(pk=id)
        elif (request.GET.get('user_name')):
            name = request.GET['user_name']
            # 查找用户名
            users = t_user.objects.filter(name = name)
        elif (request.GET.get('email')):
            email = request.GET['email']
            # 查找email
            users = t_user.objects.filter(email = email)
        if users:
            user = users[0]
        s = getUser_s(user)
        response = HttpResponse(json.dumps(s), content_type="application/json")
        return response

    else:
        return HttpResponse('只接受GET请求')
def changeinfo(request):
    if request.method == 'POST':
        av = request.FILES.get('file',None)
        msg = ''
        is_success = 0
        nickname=None
        intro=None
        user_id = request.session.get('user_id', '')
        if not user_id:
            msg = '您未登录！'
            is_success = -1
        else:
            user= t_user.objects.filter(pk=user_id).first()
            if user:
                if request.POST.get('nickname'):
                    nickname = request.POST['nickname']
                if request.POST.get('intro'):
                    intro = request.POST['intro']
                if nickname:
                    # 检测是否有同昵称的用户
                    if not user.nickname == nickname:
                        user_sameName = t_user.objects.filter(nickname=nickname).first()
                        if user_sameName:
                            msg = '昵称已存在！'
                            is_success = -2
                        else:
                            user.nickname = nickname
                if is_success != -2:
                    if av:
                        user.avatar=av

                    if intro:
                        user.Intro = intro
                    user.save()
                    is_success = 1
                    msg = "已保存！"
            else:
                is_success = 0
                msg='无此用户！'
        s = {
            'is_success': is_success,
            'msg': msg
        }
        response = HttpResponse(json.dumps(s), content_type="application/json")
        return response

    else:
        return HttpResponse('只接受Post请求')
def myinfo(request):
    if request.method == 'GET':
        s={
            'user':[],
            'likes':[],
            'colls':[],
            'subs':[],
            'coms':[],
        }
        user_id = int(request.session.get('user_id', 0))
        if not user_id:
            return HttpResponse('您未登录！')

        user = t_user.objects.filter(pk=user_id).first()
        if user:
            s['user'] = getUser_s(user)
            likes_set = t_like.objects.filter(user=user)
            if likes_set:
                for like in likes_set:
                    s['likes'].append(getbooks(like.book))
            colls_set = t_coll.objects.filter(user=user)
            if colls_set:
                for coll in colls_set:
                    s['colls'].append(getbooks(coll.book))
            sub_set = t_user_sub.objects.filter(user_1=user)
            if sub_set:
                for sub in sub_set:
                    s['subs'].append(getUser_s(sub.user_2))
            com_set = t_com.objects.filter(user=user)
            if com_set:
                for com in com_set:
                    s['coms'].append(getCom_s_min(com))

        response = HttpResponse(json.dumps(s), content_type="application/json")
        return response

    else:
        return HttpResponse('只接受GET请求')
def getusershowinfo(request):
    if request.method == 'GET':
        s={
            'user':[],
            'likes':[],
            'colls':[],
            'subs':[],
            'coms':[],
            'works':[],
            'is_sub':0
        }
        user_id=None

        if (request.GET.get('id')):
            user_id = request.GET['id']
        if not user_id:
            return HttpResponse('未找到用户！')
        user = t_user.objects.filter(pk=user_id).first()
        if user:
            my_id = request.session.get('user_id', 0)
            me = t_user.objects.filter(pk=my_id).first()
            subObject = t_user_sub.objects.filter(user_1=me,user_2=user).first()
            if subObject:
                s['is_sub'] = 1
            # 查看用户是否设置为私密
            # t_pri=
            s['user'] = getUser_s(user)
            likes_set = t_like.objects.filter(user=user)
            if likes_set:
                for like in likes_set:
                    s['likes'].append(getbooks(like.book))
            colls_set = t_coll.objects.filter(user=user)
            if colls_set:
                for coll in colls_set:
                    s['colls'].append(getbooks(coll.book))
            sub_set = t_user_sub.objects.filter(user_1=user)
            if sub_set:
                for sub in sub_set:
                    s['subs'].append(getUser_s(sub.user_2))
            com_set = t_com.objects.filter(user=user)
            if com_set:
                for com in com_set:
                    s['coms'].append(getCom_s_min(com))
            cre_set = t_cre.objects.filter(user=user)
            if cre_set:
                for cre in cre_set:
                    art = cre.art
                    if art.index == 0:
                        book = t_book.objects.get(art_id=art)
                        s['works'].append(getbooks(book))
        response = HttpResponse(json.dumps(s), content_type="application/json")
        return response
    else:
        return HttpResponse('只接受GET请求')
def article(request):
    if request.method == 'GET':
        id = 0
        title = ''
        index = ''
        content = ''
        type = ''
        author = ''
        author_id = 0
        pub_time = ''
        book_id = ''
        chapters_name=[]
        chapters_id = []
        com_num = 0
        book_title = ''
        is_like=0
        is_coll=0
        if (request.GET.get('id')):
            id = request.GET['id']
            user_id = request.session.get('user_id',0)
            user=t_user.objects.filter(pk=user_id).first()
            work = t_art.objects.get(pk=id)
            if (work):
                id = work.id
                title = work.name
                content = work.content
                index = work.index
                pub_time = work.pub_time.strftime('%Y-%m-%d %H:%M:%S')
                book_id = work.book_id # 整本ID
                # 根据整本ID获取整本
                book = t_book.objects.get(art_id=book_id)
                book_title = book.name
                # 根据作品ID获取作者
                author_user = t_cre.objects.get(art=book_id).user

                if user:
                    if t_like.objects.filter(user=user,book=book):
                        is_like = 1
                    if t_coll.objects.filter(user=user,book=book):
                        is_coll = 1
                author =author_user.nickname
                author_id = author_user.id
                if not author:
                    author =author_user.name
                type = book.type
                com_num = work.com_num
                chapter_set = t_art.objects.filter(book_id=book_id).order_by("index")[1:]
                for chapter in chapter_set:
                    chapters_name.append(chapter.name)
                    chapters_id.append(chapter.id)

        s = {
            'id': id,
            'title': title,
            'index': index,
            'content': content,
            "pub_time":pub_time,
            'type': type,
            'author':author,
            'author_id':author_id,
            'chapters':chapters_name,
            'chapters_id':chapters_id,
            'book_id':book_id,
            'com_num':com_num,
            'book_title':book_title,
            'is_like':is_like,
            'is_coll':is_coll,

        }

        response = HttpResponse(json.dumps(s), content_type="application/json;charset=utf-8")
        return response
    else:
        return HttpResponse('只接受GET请求')
def workupload(request):
    if request.method == 'POST':
        pic = request.FILES.get('file',None)
        msg = ''
        is_success = 0
        user_id = request.session.get('user_id', '')
        if not user_id:
            return HttpResponse('您未登录！')
        else:
            is_book = True
            content=''
            book_type=""
            book_id = 0
            title = None
            if request.POST.get('book_id'):
                book_id = request.POST['book_id']
                if(str(book_id) != '0'):
                    is_book = False
            if request.POST.get('title'):
                title = request.POST['title']
            if request.POST.get('content'):
                content = request.POST['content']
            if request.POST.get('book_type'):
                book_type = request.POST['book_type']
            # print('aaaaaaa')
                # 开启事务
            with transaction.atomic():
                if title:
                    # print('bbbbbbbb')
                    index = 0
                    if not is_book:
                        last_art = t_art.objects.filter(book_id=book_id).order_by('-index').first()
                        index = last_art.index+1
                    art = t_art(name=title,index=index,com_num=0)
                    art.content = content
                    if book_id:
                        art.book_id = book_id
                    art.save()


                    if is_book:
                        art.book_id = art.id
                        art.save()
                        book = t_book(art_id=art,name=title,coll_num=0,like_num=0,type=book_type)
                        book.pic=pic
                        book.save()
                    # print('ccccccccc')
                    user = t_user.objects.get(pk=user_id)
                    cre = t_cre(user=user,art=art)
                    cre.save()
                    is_success = 1
                    msg = "发布成功！"




        s = {
            'is_success': is_success,
            'msg': msg
        }

        response = HttpResponse(json.dumps(s), content_type="application/json")
        return response

    else:
        return HttpResponse('只接受Post请求')
def workbyuser(request):
    if request.method == 'GET':
        user_id = 0
        user = None
        s = {'works':[]}
        if (request.GET.get('id')):
            id = request.GET['id']
            work_set = t_cre.objects.filter(user=id)

            if work_set:
                for work in work_set:
                    book = t_art.objects.get(book_id=work.art.book_id,index=0)
                    if work.art.id == book.id:
                        book_set = t_art.objects.filter(book_id=book.book_id).order_by('index')

                        art_set = []
                        for art in book_set:
                            art_set.append(getArts(art))
                        s['works'].append(art_set)

        response = HttpResponse(json.dumps(s), content_type="application/json;charset=utf-8")
        return response
    else:
        return HttpResponse('只接受GET请求')
from django.db.models import Q
def getworks(request):
    if request.method == 'GET':
        user_id = 0
        user = None
        s = {'works':[]}
        type = ''
        order=1
        pattern=2
        q=20
        if (request.GET.get('type')):
            type = request.GET['type']
            if type not in ['武侠', '玄幻', '都市', '军事', '游戏', '科幻', '现实', '历史', '言情', '体育', '悬疑']:
                type = ''
        if (request.GET.get('q')):
            q = int(request.GET['q'])
        if (request.GET.get('order')):
            order = int(request.GET['order'])
        if (request.GET.get('pattern')):
            pattern = int(request.GET['pattern'])
        book_set=None
        if pattern == 1:
            if order == 1:
                # print('book_set')
                book_set = t_book.objects.filter(Q(type__icontains=type)).order_by('like_num')
            else:
                book_set = t_book.objects.filter(Q(type__icontains=type)).order_by('-like_num')
        elif pattern == 2:
                book_set = t_book.objects.filter(Q(type__icontains=type))
        elif pattern == 3:
            if order == 1:
                book_set = t_book.objects.filter(Q(type__icontains=type)).order_by('coll_num')
            else:
                book_set = t_book.objects.filter(Q(type__icontains=type)).order_by('-coll_num')
        art_set = []

        if book_set:
            for book in book_set:
                art_set.append(getbooks(book))
        if art_set:
            if len(art_set) > q:
                art_set = art_set[0:q]
            s['works']=art_set

        response = HttpResponse(json.dumps(s), content_type="application/json;charset=utf-8")
        return response
    else:
        return HttpResponse('只接受GET请求')

def artsearch(request):
    if request.method == 'GET':
        user_id = 0
        user = None
        s = {'works':[]}
        type = ''
        order=1
        pattern=2
        q=100
        if (request.GET.get('key')):
            key = request.GET['key']
        # if (request.GET.get('q')):
        #     q = int(request.GET['q'])
        # if (request.GET.get('order')):
        #     order = int(request.GET['order'])
        book_set=None
        book_set = t_book.objects.filter(Q(name__icontains=key)).order_by('-like_num', '-coll_num')
        art_set=[]
        if book_set:
            for book in book_set:
                art_set.append(getbooks(book))
        art_set=sorted(art_set, key=lambda x:x["pub_time"], reverse=False)
        if art_set:
            if len(art_set) > q:
                art_set = art_set[0:q]
            s['works']=art_set

        response = HttpResponse(json.dumps(s), content_type="application/json;charset=utf-8")
        return response
    else:
        return HttpResponse('只接受GET请求')

def usersearch(request):
    if request.method == 'GET':
        s = {'users':[]}
        type = ''
        order=1
        pattern=2
        q=100
        if (request.GET.get('key')):
            key = request.GET['key']
        # if (request.GET.get('q')):
        #     q = int(request.GET['q'])
        # if (request.GET.get('order')):
        #     order = int(request.GET['order'])
        user_set=None
        user_set = t_user.objects.filter(Q(nickname__icontains=key))
        users=[]
        if user_set:
            for user in user_set:
                users.append(getUser_s(user))
        if users:
            if len(users) > q:
                users = users[0:q]
            s['users']=users
        response = HttpResponse(json.dumps(s), content_type="application/json;charset=utf-8")
        return response
    else:
        return HttpResponse('只接受GET请求')

def addlike(request):
    if request.method == 'GET':
        msg=''
        is_success = 0
        user_id=int(request.session.get('user_id', 0))
        if not user_id:
            msg='您未登录！'
            is_success=-1
        art_id = int(request.GET.get('id',0))
        if art_id and user_id:
            art = t_art.objects.get(pk=art_id)
            book =t_book.objects.get(art_id=art)
            user = t_user.objects.get(pk=user_id)
            if art and user and book:
                try:
                    # 开启事务
                    with transaction.atomic():
                        likeObject=t_like.objects.filter(book=book,user=user).first()
                        if likeObject:
                            book.like_num -=1
                            book.save()
                            likeObject.delete()
                            msg = '取消点赞成功！'
                            is_success = 1
                        else:
                            likeObject=t_like(book=book,user=user)
                            # 整本点赞数增1
                            book.like_num +=1
                            book.save()
                            likeObject.save()
                            msg = '点赞成功！'
                            is_success = 1
                except Exception as e:
                    return HttpResponse("数据库更新错误<%s>" % str(e))
            else:
                msg='操作错误！'
                is_success=0
        s={
            'msg':msg,
            'is_success':is_success
        }
        response = HttpResponse(json.dumps(s), content_type="application/json;charset=utf-8")
        return response
    else:
        return HttpResponse('只接受GET请求')

def addcoll(request):
    if request.method == 'GET':
        msg=''
        is_success = 0
        user_id=int(request.session.get('user_id', 0))
        if not user_id:
            msg='您未登录！'
            is_success=-1
        art_id = int(request.GET.get('id',0))
        if art_id and user_id:
            art = t_art.objects.get(pk=art_id)
            book =t_book.objects.get(art_id=art)
            user = t_user.objects.get(pk=user_id)
            if art and user and book:
                try:
                    # 开启事务
                    with transaction.atomic():
                        collObject=t_coll.objects.filter(book=book,user=user).first()
                        if collObject:
                            book.coll_num -=1
                            book.save()
                            collObject.delete()
                            msg = '取消收藏成功！'
                            is_success = 1
                        else:
                            collObject=t_coll(book=book,user=user)
                            # 整本收藏数增1
                            book.coll_num +=1
                            book.save()
                            collObject.save()
                            msg = '收藏成功！'
                            is_success = 1
                except Exception as e:
                    return HttpResponse("数据库更新错误<%s>" % str(e))
            else:
                msg='操作错误！'
                is_success=0
        s={
            'msg':msg,
            'is_success':is_success
        }
        response = HttpResponse(json.dumps(s), content_type="application/json;charset=utf-8")
        return response
    else:
        return HttpResponse('只接受GET请求')

def addsub(request):
    if request.method == 'GET':
        msg=''
        is_success = 0
        user_id=int(request.session.get('user_id', 0))
        if not user_id:
            msg='您未登录！'
            is_success=-1
        else:
            user2_id = int(request.GET.get('id',0))
            if user2_id and user_id:
                if user2_id == user_id:
                    msg = '不能订阅自己！'
                    is_success = -2
                else:
                    user1 = t_user.objects.filter(pk=user_id).first()
                    user2 = t_user.objects.filter(pk=user2_id).first()
                    if user1 and user2:
                        # 开启事务
                        with transaction.atomic():
                            subObject=t_user_sub.objects.filter(user_1=user1,user_2=user2).first()
                            if subObject:
                                subObject.delete()
                                msg = '取消订阅成功！'
                                is_success = 1
                            else:
                                subObject=t_user_sub(user_1=user1,user_2=user2)
                                subObject.save()
                                msg = '订阅成功！'
                                is_success = 1

            else:
                msg='操作错误！'
                is_success=0
        s={
            'msg':msg,
            'is_success':is_success
        }
        response = HttpResponse(json.dumps(s), content_type="application/json;charset=utf-8")
        return response
    else:
        return HttpResponse('只接受GET请求')

def getArts(art):
    s = {}
    if art:
        s = {
            'id':art.id,
            'title':art.name,
            'index':art.index,
        }
    return s

def getbooks(book):
    s = {}
    if book:
        art = t_art.objects.get(id = book.art_id.id)
        user = t_cre.objects.get(art=art).user
        s = {
            'pic':str(book.pic),
            'type':book.type,
            'id':art.id,
            'title':art.name,
            'content':art.content,
            'com_num':art.com_num,
            "pub_time":art.pub_time.strftime('%Y-%m-%d %H:%M:%S'),
            'user':getUser_s(user)
        }
    return s


def userbywork(request):
    if request.method == 'GET':
        user_id = 0
        user = None
        s = {}
        if (request.GET.get('id')):
            id = request.GET['id']
            user_cre_set = t_cre.objects.filter(art=id)
            user_cre = None
            if(user_cre_set):
                user_cre = user_cre_set[0]
            if user_cre:
                user_id = user_cre.user.id
                user_set = t_user.objects.filter(pk=user_id)
                if user_set:
                    user = user_set[0]
                    s = getUser_s(user)

        response = HttpResponse(json.dumps(s), content_type="application/json;charset=utf-8")
        return response
    else:
        return HttpResponse('只接受GET请求')

def comment(request):

    if request.method == 'POST':
        msg = ''
        is_success = 0
        user_id = request.session.get('user_id', '')
        if not user_id:
            is_success = -1
        else:
            art_id =None
            rep_user =0
            anc_comment =None
            content=''
            if request.POST.get('art_id'):
                art_id = request.POST['art_id']
            if request.POST.get('anc_comment'):
                anc_comment = request.POST['anc_comment']
            if request.POST.get('rep_user'):
                rep_user = request.POST['rep_user']
            if request.POST.get('content'):
                content = request.POST['content']
            article = t_art.objects.get(pk=art_id)
            try:
                # 开启事务
                with transaction.atomic():
                    # 评论数增1
                    article.com_num = article.com_num+1
                    article.save()
            except Exception as e:
                return HttpResponse("数据库更新错误<%s>" % str(e))


            user = t_user.objects.get(pk=user_id)
            comment = t_com(art=article)
            comment.anc_com = anc_comment
            comment.rep_user = rep_user
            comment.content = content
            comment.user = user
            comment.like_num = 0
            comment.save()

            is_success = 1
            msg = "评论成功"

        s = {
            'is_success': is_success,
            'msg': msg
        }

        response = HttpResponse(json.dumps(s), content_type="application/json")
        return response

    else:
        return HttpResponse('只接受Post请求')

def getcomment(request):
    if request.method == 'GET':
        s = {'comment':[]}
        if (request.GET.get('art_id')):
            art_id = request.GET['art_id']
            article = t_art.objects.get(pk=art_id)
            comment_set = t_com.objects.filter(Q(art=article),Q(anc_com=None)|Q(anc_com=0)).order_by('-pub_time')
            for com in comment_set:
                com_s = getCom_s(com)
                com_s['reply'] = []
                # 循环查找子评论：
                for rep in t_com.objects.filter(anc_com=com.id).order_by('pub_time'):
                    com_s['reply'].append(getCom_s(rep))
                s['comment'].append(com_s)

        response = HttpResponse(json.dumps(s), content_type="application/json;charset=utf-8")
        return response
    else:
        return HttpResponse('只接受GET请求')

def getUser_s(user):
    s = {}
    if user:
        s = {

            'name':user.name,
            'nickname':user.nickname,
            'id':user.id,
            'avatar':str(user.avatar),
            "intro":user.Intro,
            'login_time':user.last_login_time.strftime('%Y-%m-%d %H:%M:%S'),
        }
    return s

def getCom_s_min(com):
    s = {}
    if com:
        s = {
            'content': com.content,
            'art_title':com.art.name,
            'id': com.id,
            'art_id':com.art.id,
            'pub_time': com.pub_time.strftime('%Y-%m-%d %H:%M:%S'),
            'like_num': com.like_num

        }
        if com.rep_user:
            rep_user = t_user.objects.get(pk=com.rep_user)
            s['rep_user'] = com.rep_user
            if rep_user.nickname:
                s['rep_user_name'] = rep_user.nickname
            else:
                s['rep_user_name'] = rep_user.name
    return s

def getCom_s(com):
    s = {}
    if com:
        s = {
            'user': getUser_s(com.user),
            'content': com.content,
            'id': com.id,
            'pub_time': com.pub_time.strftime('%Y-%m-%d %H:%M:%S'),
            'like_num': com.like_num
        }
        if com.rep_user:
            rep_user=t_user.objects.get(pk=com.rep_user)
            s['rep_user']= com.rep_user
            if rep_user.nickname:
                s['rep_user_name']=rep_user.nickname
            else:
                s['rep_user_name']=rep_user.name
    return s
from project import settings
def test(request):
    return HttpResponse(settings.MEDIA_ROOT)