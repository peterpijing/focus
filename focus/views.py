# coding=utf-8
from django.shortcuts import render

# Create your views here.
# veiws.py用于封装负责处理用户请求及返回响应的逻辑。

from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Comment, Poll, NewUser
from .forms import CommmentForm, LoginForm, RegisterForm, SetInfoForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.cache import cache_page

import markdown2, urlparse


from forms import LoginForm
def index(request):
    # Article.objects.query_by_time()
    # 这个涉及到django模型类的管理器的知识,在models.py中自定义一个Article模型的管理器ArticleManager
    latest_article_list = Article.objects.query_by_time()
    loginform = LoginForm()
    context = {'latest_article_list': latest_article_list, 'loginform':loginform}
    return render(request, 'index.html', context)


def log_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['uid']
            password = form.cleaned_data['pwd']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                url = request.POST.get('source_url', '/focus')
                return redirect(url)
            else:
                return render(request, 'login.html', {'form': form, 'error': "password or username is not ture!"})

        else:
            return render(request, 'login.html', {'form': form})

# @login_required这个装饰器是django内置的，它的作用是使所装饰的函数必须是登录的用户才继续运行，
# 不然进入指定的login_url, 参见 django 文档 , 我们这里没有指定login_url，所以在settings.py中添加以下代码：
@login_required
def log_out(request):
    url = request.POST.get('source_url', '/focus/')
    logout(request)
    return redirect(url)


def article(request, article_id):
    '''
    try:   # since visitor input a url with invalid id
        article = Article.objects.get(pk=article_id)  # pk???
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    ''' # shortcut:
    article = get_object_or_404(Article, id=article_id)
    content = markdown2.markdown(article.content, extras=["code-friendly",
        "fenced-code-blocks", "header-ids", "toc", "metadata"])
    commentform = CommmentForm()
    loginform = LoginForm()
    comments = article.comment_set.all

    return render(request, 'article_page.html', {
        'article': article,
        'loginform':loginform,
        'commentform':commentform,
        'content': content,
        'comments': comments
        })


@login_required
def comment(request, article_id):
    form  = CommmentForm(request.POST)
    url = urlparse.urljoin('/focus/', article_id)
    if form.is_valid():
        user = request.user
        article = Article.objects.get(id=article_id)
        new_comment = form.cleaned_data['comment']
        c = Comment(content=new_comment, article_id=article_id)  # have tested by shell
        c.user = user
        c.save()
        article.comment_num += 1
    return redirect(url)

@login_required
def get_keep(request, article_id):
    logged_user = request.user
    article = Article.objects.get(id=article_id)

    # 因为文章与用户是多对多关系，所以logged_user.article_set.all()
    # 会得到这个登录用户对应的所有文章(即它收藏的文章)
    articles = logged_user.article_set.all()
    if article not in articles:
        article.user.add(logged_user)  # for m2m linking, have tested by shell
        article.keep_num += 1
        article.save()

        return redirect('/focus/')
    else:
        url = urlparse.urljoin('/focus/', article_id)
        return redirect(url)

@login_required
def get_poll_article(request,article_id):
    logged_user = request.user
    article = Article.objects.get(id=article_id)
    polls = logged_user.poll_set.all()
    articles = []
    for poll in polls:
        articles.append(poll.article)

    if article in articles:
        url = urlparse.urljoin('/focus/', article_id)
        return redirect(url)
    else:
        article.poll_num += 1
        article.save()
        poll = Poll(user=logged_user, article=article)
        poll.save()
        data = {}
        return redirect('/focus/')

def register(request):
    # 第2，3 行，定义两个错误提示信息
    error1 = "this name is already exist"
    valid = "this name is valid"

    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if request.POST.get('raw_username', 'erjgiqfv240hqp5668ej23foi') != 'erjgiqfv240hqp5668ej23foi':  # if ajax
            try:
                user = NewUser.objects.get(username=request.POST.get('raw_username', ''))
            except ObjectDoesNotExist:
                return render(request, 'register.html', {'form': form, 'msg': valid})
            else:
                return render(request, 'register.html', {'form': form, 'msg': error1})

        else:
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if password1 != password2:
                    return render(request, 'register.html', {'form': form, 'msg': "two password is not equal"})
                else:
                    user = NewUser(username=username, email=email, password=password1)
                    user.save()
                    # return render(request, 'login.html', {'success': "you have successfully registered!"})
                    return redirect('/focus/login')
            else:
                return render(request, 'register.html', {'form': form})