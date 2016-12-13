#coding=utf-8
from django import forms

# Widget 是Django 对HTML 输入元素的表示
# 其中’class’ ＝ ‘form-control’ 是因为我们前端模版的css定义好了这种‘class’的style，‘placeholder’是html的知识
class LoginForm(forms.Form):
    uid = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control' ,'id':'uid', 'placeholder': 'Username'}))
    pwd = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control' ,'id':'pwd', 'placeholder': 'Password'}))


# 渲染到注册页面(register.html，此文件请自行编写) 则有onblur ＝’authentication()‘ ，
# 这个onblur是html语法中指定鼠标离开这个元素所执行的js函数，

class RegisterForm(forms.Form):
    username = forms.CharField(label='username', max_length=100,
                               widget=forms.TextInput(attrs={'id': 'username', 'onblur': 'authentication()'}))
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
'''

<script>
function authentication(){
    var raw_username = document.getElementById("username").value;
    $.ajax({type:'POST', data: {'raw_username': raw_username}
    });
};
</script>
定义authentication()函数，虽然只是一个函数，但是涉及到了js，jQuery, AJAX, 所以我们一步步讲：

‘var raw_username‘ 定义一个变量，document.getElementById(“username”).value 得到用户输入的用户名。

$.ajax是jQuery AJAX 方法，参阅 这里， 这个方法会以post的方式传递一个数据{‘raw_username’: raw_username} 给相应的处理函数。
'''


class SetInfoForm(forms.Form):
    username = forms.CharField()


class CommmentForm(forms.Form):
    comment = forms.CharField(label='', widget=forms.Textarea(attrs={'cols': '60', 'rows': '6'}))


class SearchForm(forms.Form):
    keyword = forms.CharField(widget=forms.TextInput)