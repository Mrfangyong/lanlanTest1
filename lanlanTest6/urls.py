"""lanlanTest6 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url,include
from app01.views import  index,login,register,logout,search_book_page,search_result,search_word,crawler_result,collect_l,del_l,word_collect,del_word,search_picture
from app01.views import  picture_result,search_issue
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    url('admin/', admin.site.urls),
    url(r"^index",index),
    url(r"^login",login),
    url(r"^register",register),
    url(r"^logout",logout),
    url(r"^captcha",include("captcha.urls")),
    #书籍类别
    url(r"^search_book_page",search_book_page),
    url(r"^search_result",search_result),
    url(r'^collect_l/$', collect_l, name='collect_l'),
    url(r"^del_l/$",del_l,name="del_l"),
    #其他类别
    url(r"^search_word",search_word),
    url(r"^word_collect/$",word_collect,name='word_collect'),
    url(r"^del_word/$",del_word,name="del_word"),
    url(r"^crawler_result",crawler_result),
    url(r"^search_issue",search_issue),
    
    
    #图片搜索
    url(r"^search_picture",search_picture),
    url(r"^picture_result",picture_result)
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
