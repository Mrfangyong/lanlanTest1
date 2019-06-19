from django.shortcuts import render, redirect
from .models import User,content_table,crawler_data,IMG
from .forms import UserForm,RegisterForm
from django.db import connection
# Create your views here.
from django.http import HttpResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

import time
from django.db.models import Q
# Create your views here.
# 保留用户操作
def insert_history(request):
    user=request.session.get("user_name")
    action=request.session.get("cont1")
    plate=request.session.get("plate")
    time=request.session.get("now_time")
    cursor=connection.cursor()
    sql="insert  into app01_history_table (account,time,action,plate) values('%s','%s','%s','%s')"%(user,time,action,plate) 
    cursor.execute(sql)
    


def index(request):
    return render(request,"login/index.html")
def login(request):
    state=True
    char="@#$%^&*(){}!|<>?"
    if request.session.get("is_login",None):
        return redirect("/index")
    if request.method=="POST":
        login_form=UserForm(request.POST) #post方法接受表单数据，并验证
        if login_form.is_valid():  #数据验证工作
            username=request.POST.get("username",None)
            password=request.POST.get("password",None)
            for c in char:
                if c in username:
                    state=False
            if state==False:
                message="用户名包含特殊字符，请检查！！！"
            else:
                try:
                    user=User.objects.get(name=username)
                    request.session["is_login"]=True
                    request.session["user_name"]=user.name
                    user_name=request.session.get("user_name")
                    if user.password==password:
                        return redirect("/index/")
                    else:
                        message="密码不正确"
                except:
                    message="用户名不存在"
        return render(request,"login/login.html",locals())# locals() 返回当前所有的本地变量字典
    login_form=UserForm()
    return render(request,"login/login.html",locals())
def register(request):
    if request.session.get("is_login",None):
        return redirect("/index")
    
    if request.method=="POST":
        register_form=RegisterForm(request.POST)
        message="请检查填写的内容"
        if register_form.is_valid():
            username=register_form.cleaned_data["username"]
            password1=register_form.cleaned_data["password1"]
            password2=register_form.cleaned_data["password2"]
            email=register_form.cleaned_data["email"]
            sex=register_form.cleaned_data["sex"]
            if password1!=password2:
                message="两次密码输入不同！！"
                return render(request,"login/register.html",locals())
            else:
                same_name_user=User.objects.filter(name=username)
                if same_name_user:
                    message="用户已经存在，请重新选择用户名"
                    return render(request,"login/register.html",locals())
                same_email_user=User.objects.filter(email=email)
                if same_email_user:
                    message="该邮箱地址已被注册，请使用别的邮箱"
                    return render(request,"login/register.html",locals())
                new_user=User.objects.create()
                new_user.name=username
                new_user.password=password1
                new_user.email=email
                new_user.sex=sex
                new_user.save()
                return redirect("/login/")#自动跳转到登陆页面
    register_form=RegisterForm()
    return render(request,"login/register.html",locals()) 
def logout(request): # 登出   
    if not request.session.get("is_login",None):
        return redirect("/index")
    request.session.flush() # 一次性清空session中的所有内容
    return redirect("/index")

def search_book_page(request):
    a=1
    if a==1:
        request.session["plate"]="虚构类"
    if not request.session.get("is_login",None):
        return redirect("/index/")
    return render(request,"login/search_book_result_page.html")

#多关键字处理方法
def pinjie(word):
    words=word.replace("，",",")
    if words.__contains__(","):
        word_list=words.split(",")
        return word_list
    else:
        return words
def get_cursor(sql):
    cursor=connection.cursor()
    cursor.execute(sql)
    row = cursor.fetchall()
    content_list=[]
    for i in row:
        content_list.append(list(i))
    return content_list
def search_result(request):
    cont1=""
    if request.POST:
        cont1=request.POST["cont1"]
    else:
        cont1=request.session.get("cont1")
    if cont1=="":
        message="请输入关键字查询"
        return render(request,"login/search_book_result_page.html",{"message":message})
    request.session["cont1"]=cont1
    now_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    request.session["now_time"]=now_time
    cont1=pinjie(cont1)
    sql="SELECT translate,id,collection_nums,delete_flag FROM app01_content_table WHERE MATCH (content,translate) AGAINST ('%s' IN NATURAL LANGUAGE MODE) limit 1000 "%cont1
    print(sql)
    content_list=get_cursor(sql)
    paginator = Paginator(content_list,10,3)
    insert_history(request)
    try: 
        num = request.GET.get('index','1') 
        number = paginator.page(num)
    except PageNotAnInteger: 
        number = paginator.page(1) 
    except EmptyPage: 
        number = paginator.page(paginator.num_pages) 
        # 将当前页页码，以及当前页数据传递到index.html 
    time.sleep(0.5)
    return render(request,"login/search_result.html",{'page':number,"articles":paginator})

# 收藏方法
def collect_l(request):
    if request.method == 'POST':
        sc_id=request.POST.get('sc_id') 
        cursor=connection.cursor()
        plate=request.session.get("plate")
        i=0
        if i==0:
            request.session["cont1"]="收藏成功_"+sc_id+"_"+plate
            insert_history(request)    
        sql="update app01_content_table set collection_nums=collection_nums+1 where id =%s "%sc_id
        cursor.execute(sql)
           
        return HttpResponse("内容收藏成功")     #最后返会给前端的数据，如果能在前端弹出框中显示我们就成功了
    else:
        return HttpResponse("<h1>test</h1>")
# 删除方法
def del_l(request):
    if request.method == 'POST':
        sc_id=request.POST.get('sc_id') 
        cursor=connection.cursor()
        plate=request.session.get("plate")
        i=0
        if i==0:
            request.session["cont1"]="报错成功_"+sc_id+"_"+plate
            insert_history(request)    
        sql1="update app01_content_table set delete_flag=1 where id =%s"%sc_id
        cursor.execute(sql1)
        return HttpResponse("内容报错成功")     #最后返会给前端的数据，如果能在前端弹出框中显示我们就成功了
    else:
        return HttpResponse("<h1>test</h1>")
    
    
# 爬虫搜搜
def search_word(request):
    if not request.session.get("is_login",None):
        return redirect("/index/")
    cursor=connection.cursor()
    sql="SELECT * FROM  app01_article_type_table"
    cursor.execute(sql)
    row = cursor.fetchall()
    name=[]
    id=[]
    for i in row:
        id.append(i[0])
        name.append("".join(list(i[1])))
    dict1={"ids":id,"names":dict(row)}
    return render(request,"login/search_page.html",dict1)
def crawler_result(request):
    type_id=request.POST.get("box")
    cont=request.POST.get("cont")
    section=request.POST.get("section")
    request.session["type_id"]=type_id
    request.session["cont"]=cont
    request.session["section"]=section
    global word_object
    if str(type_id)!="-1":
        if section=="1":
            sql="select id,contents,question,collection_nums,delete_flag  from app01_crawler_data WHERE MATCH (contents,question) AGAINST ('%s' IN NATURAL LANGUAGE MODE) and type_id=%s  and length>100 and length<200"%(cont,type_id)       
            word_object=get_cursor(sql)
            insert_history(request)
        elif section=="2":
            sql="select id,contents,question,collection_nums,delete_flag  from app01_crawler_data WHERE MATCH (contents,question) AGAINST ('%s' IN NATURAL LANGUAGE MODE) and type_id=%s  and length>200 and length<400"%(cont,type_id)       
            word_object=get_cursor(sql)
            insert_history(request)
        elif section=="3":
            sql="select id,contents,question,collection_nums,delete_flag  from app01_crawler_data WHERE MATCH (contents,question) AGAINST ('%s' IN NATURAL LANGUAGE MODE) and type_id=%s  and length>400 and length<800"%(cont,type_id)       

            word_object=get_cursor(sql)
            insert_history(request)
        elif section=="4":
            sql="select id,contents,question,collection_nums,delete_flag  from app01_crawler_data WHERE MATCH (contents,question) AGAINST ('%s' IN NATURAL LANGUAGE MODE) and type_id=%s  and length>800"%(cont,type_id)       

            word_object=get_cursor(sql)
            insert_history(request)
        elif section=="-1":
            sql="select id,contents,question,collection_nums,delete_flag  from app01_crawler_data WHERE MATCH (contents,question) AGAINST ('%s' IN NATURAL LANGUAGE MODE) and type_id=%s "%(cont,type_id)       

            word_object=get_cursor(sql)
            insert_history(request)
        paginator = Paginator(word_object,10,3)  
        a=2
        if a==2:
            request.session["plate"]="非虚构类"
        request.session["cont1"]=cont
        now_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        request.session["now_time"]=now_time
        insert_history(request)
        try: 
            num = request.GET.get('index','1') 
            number = paginator.page(num)
        except PageNotAnInteger: 
            number = paginator.page(1) 
        except EmptyPage: 
            number = paginator.page(paginator.num_pages) 
            # 将当前页页码，以及当前页数据传递到index.html 
        time.sleep(0.5)
        return render(request,"login/word_result.html",{'page':number,"articles":paginator})
    else:
        print("*****进来了")
        if section=="1":
            sql="select id,contents,question,collection_nums,delete_flag  from app01_crawler_data WHERE MATCH (contents,question) AGAINST ('%s' IN NATURAL LANGUAGE MODE)   and length>100 and length<200"%(cont)       
            word_object=get_cursor(sql)
            insert_history(request)
        elif section=="2":
            sql="select id,contents,question,collection_nums,delete_flag  from app01_crawler_data WHERE MATCH (contents,question) AGAINST ('%s' IN NATURAL LANGUAGE MODE)   and length>200 and length<400"%(cont)       
            word_object=get_cursor(sql)
            insert_history(request)
        elif section=="3":
            sql="select id,contents,question,collection_nums,delete_flag  from app01_crawler_data WHERE MATCH (contents,question) AGAINST ('%s' IN NATURAL LANGUAGE MODE)  and length>400 and length<800"%(cont)       

            word_object=get_cursor(sql)
            insert_history(request)
        elif section=="4":
            sql="select id,contents,question,collection_nums,delete_flag  from app01_crawler_data WHERE MATCH (contents,question) AGAINST ('%s' IN NATURAL LANGUAGE MODE)  and length>800"%(cont)       

            word_object=get_cursor(sql)
            insert_history(request)
        elif section=="-1":
            sql="select id,contents,question,collection_nums,delete_flag  from app01_crawler_data WHERE MATCH (contents,question) AGAINST ('%s' IN NATURAL LANGUAGE MODE) "%(cont)       
            word_object=get_cursor(sql)
            insert_history(request)
        paginator = Paginator(word_object,10,3)  
        request.session["cont1"]=cont
        now_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        request.session["now_time"]=now_time
        insert_history(request)
        try: 
            num = request.GET.get('index','1') 
            number = paginator.page(num)
        except PageNotAnInteger: 
            number = paginator.page(1) 
        except EmptyPage: 
            number = paginator.page(paginator.num_pages) 
            # 将当前页页码，以及当前页数据传递到index.html 
        time.sleep(0.5)
        return render(request,"login/word_result.html",{'page':number,"articles":paginator})
    
    
def word_collect(request):
    
    if request.method == 'POST':
        sc_id=request.POST.get('sc_id') 
        cursor=connection.cursor()
        plate=request.session.get("plate")
        i=0
        if i==0:
            request.session["cont1"]="收藏成功_"+sc_id+"_"+plate
            insert_history(request)       
        sql="update app01_crawler_data set collection_nums=collection_nums+1 where id =%s"%sc_id
        cursor.execute(sql)   
        return HttpResponse("内容收藏成功")     #最后返会给前端的数据，如果能在前端弹出框中显示我们就成功了
    else:
        return HttpResponse("<h1>收藏失败</h1>")

# 删除方法
def del_word(request):
    if request.method == 'POST':
        sc_id=request.POST.get('sc_id') 
        cursor=connection.cursor()
        plate=request.session.get("plate")
        i=0
        if i==0:
            request.session["cont1"]="报错成功_"+sc_id+"_"+plate
            insert_history(request)      
        sql1="update app01_crawler_data set delete_flag=1 where id =%s"%sc_id
        cursor.execute(sql1)
        return HttpResponse("内容报错成功")     #最后返会给前端的数据，如果能在前端弹出框中显示我们就成功了
    else:
        return HttpResponse("<h1>test</h1>") 


# 搜索问题
def search_issue(request):
    issue=""
    if request.POST:
        issue=request.POST["headline"]
    else:
        issue=request.session.get("issue")
    request.session["issue"]=issue
        
    sql="select id,contents,question,collection_nums,delete_flag from app01_crawler_data where question='%s' "%issue
    print(sql)
    result_L=get_cursor(sql)
    paginator = Paginator(result_L,5,3)  
    insert_history(request)
    try: 
        num = request.GET.get('index','1') 
        number = paginator.page(num)
    except PageNotAnInteger: 
        number = paginator.page(1) 
    except EmptyPage: 
        number = paginator.page(paginator.num_pages) 
        # 将当前页页码，以及当前页数据传递到index.html 
    return render(request,"login/issue.html",{'page':number,"articles":paginator})
  
 #  近义词 ：  喜欢  ++    仰慕 ， 崇拜    
 
 
def search_picture(request):
    return render(request,"login/search_picture_page.html")
from django.http import HttpResponseRedirect
from django.http import HttpResponse
def picture_result(request):
    print("99999")
    name=request.POST.get("name")
    print(name)
    imgs = IMG.objects.filter(name=name)
    content = {
        'imgs':imgs,
    }
    for i in imgs:
        print (i.img.url)
    return HttpResponseRedirect("/index")
#     return render(request, 'login/picture_result.html', content)













