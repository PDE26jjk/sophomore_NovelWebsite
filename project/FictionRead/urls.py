from django.urls import path,re_path
from . import  views
from django.views.static import  serve
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('userstation.action/',views.userstation),
    path('login.action/',views.login),
    path('logout.action/',views.logout),
    path('register.action/',views.register),
    path('verification.action/',views.verification),
    path('userinfo.action/',views.userinfo),
    path('myinfo.action/',views.myinfo),
    path('getusershowinfo.action/',views.getusershowinfo),

    path('changeinfo.action/',views.changeinfo),

    path('comment.action/',views.comment),
    path('getcomments.action/',views.getcomment),


    path('artsearch.action/',views.artsearch),
    path('usersearch.action/',views.usersearch),

    path('article.action/',views.article),
    path('userbywork.action/',views.userbywork),

    path('workbyuser.action/',views.workbyuser),
    path('workupload.action/',views.workupload),
    path('getworks.action/',views.getworks),

    path('addlike.action/',views.addlike),
    path('addcoll.action/',views.addcoll),
    path('addsub.action/',views.addsub),

    # path('test/',views.test),
    # 媒体文件，如 域名/media/avatar/default.png
    re_path(r"^media/(?P<path>.*)", serve, {"document_root": settings.MEDIA_ROOT}),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
