from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import render, redirect

from app02 import models


def depart_list(request):
    """ 部门列表 """

    # 创建数据
    # Department.objects.create(id="1", title="英语学习部")
    # Department.objects.create(id="2", title="IT运维部门")
    # Department.objects.create(id="3", title="媒体企划")

    # 去数据库中获取所有的部门列表
    #  [对象,对象,对象]
    queryset = models.Department.objects.all()

    return render(request, 'depart_list.html', {'queryset': queryset})


def depart_init_add(request):
    """ 添加部门（一键添加） """

    # 创建初始测试数据
    init_depart_list = ["集中营运产品部", "基础平台部", "资负预财部", "IT维护部", "网络安全部", "英语学习部"]
    # 添加到数据库中
    for department_name in init_depart_list:
        # 解包数据
        models.Department.objects.create(title=department_name)

    # 返回到用户列表页面
    return redirect("/depart/list/")


def depart_add(request):
    """ 添加部门 """
    if request.method == "GET":
        return render(request, 'depart_add.html')

    # 获取用户POST提交过来的数据（title输入为空）
    title = request.POST.get("title")

    # 保存到数据库
    models.Department.objects.create(title=title)

    # 重定向回部门列表
    return redirect("/depart/list/")


def depart_delete(request):
    """ 删除部门 """
    # 获取ID http://127.0.0.1:8000/depart/delete/?nid=1
    nid = request.GET.get('nid')

    # 删除
    models.Department.objects.filter(id=nid).delete()

    # 重定向回部门列表
    return redirect("/depart/list/")


def depart_edit(request, nid):
    """ 修改部门 """
    if request.method == "GET":
        # 根据nid，获取他的数据 [obj,]
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {"row_object": row_object})

    # 获取用户提交的标题
    title = request.POST.get("title")

    # 根据ID找到数据库中的数据并进行更新
    # models.Department.objects.filter(id=nid).update(title=title,其他=123)
    models.Department.objects.filter(id=nid).update(title=title)

    # 重定向回部门列表
    return redirect("/depart/list/")


def user_list(request):
    """ 用户管理 """

    # 获取所有用户列表 [obj,obj,obj]
    queryset = models.UserInfo.objects.all()
    """
    # 用Python的语法获取数据
    for obj in queryset:
        print(obj.id, obj.name, obj.account, obj.create_time.strftime("%Y-%m-%d"), obj.gender, obj.get_gender_display(), obj.depart_id, obj.depart.title)
        # print(obj.name, obj.depart_id)
        # obj.depart_id  # 获取数据库中存储的那个字段值
        # obj.depart.title  # 根据id自动去关联的表中获取哪一行数据depart对象。
    """
    return render(request, 'user_list.html', {"queryset": queryset})


def user_delete(request):
    """ 删除用户"""
    # 获取ID http://127.0.0.1:8000/user/delete/?nid=1
    nid = request.GET.get('nid')

    # 删除
    models.UserInfo.objects.filter(id=nid).delete()

    # 重定向回部门列表
    return redirect("/user/list/")


def user_add(request):
    """ 添加用户（原始方式） """

    if request.method == "GET":
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            "depart_list": models.Department.objects.all()
        }
        return render(request, 'user_add.html', context)

    # 获取用户提交的数据
    if request.method == "POST":
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        age = request.POST.get('age')
        account = request.POST.get('ac')
        ctime = request.POST.get('ctime')
        gender = request.POST.get('gd')
        depart_id = request.POST.get('dp')

        # 添加到数据库中
        models.UserInfo.objects.create(name=user, password=pwd, age=age,
                                       account=account, create_time=ctime,
                                       gender=gender, depart_id=depart_id)

        # 返回到用户列表页面
        return redirect("/user/list/")


def user_init_add(request):
    """ 添加用户（一键添加） """

    # 创建初始测试数据
    init_user_list = [
        ("韩超", "666", 23, 100.68, "2020-01-11", 2, 1),
        ("刘东", "123", 23, 100.68, "2010-11-11", 1, 4),
        ("朱虎飞", "999", 33, 9900.68, "2021-05-11", 1, 1),
        ("Barry", "311", 32, 7777777, "2004-08-06", 1, 1),
        ("Mechelle", "9124124", 65, 8888888, "1888-12-24", 1, 1),
        ("周亚男", "912412s", 23, 9999999, "1995-03-10", 1, 1),
        ("黄飞鸿", "gsdgdsfg", 13, 22222222.22, "2024-12-11", 1, 1),
    ]
    # 添加到数据库中
    for data in init_user_list:
        # 解包数据
        name, password, age, account, create_time, gender, depart_id = data
        models.UserInfo.objects.create(name=name, password=password, age=age,
                                       account=account, create_time=create_time,
                                       gender=gender, depart_id=depart_id)

    # 返回到用户列表页面
    return redirect("/user/list/")


# ################################# ModelForm 示例 #################################
from django import forms


class UserModelForm(forms.ModelForm):
    name = forms.CharField(min_length=3, label="用户名")

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", 'account', 'create_time', "gender", "depart"]

        '''需要给ModelForm自动生成的form添加样式'''

        '''方法一： 通过插件widgets给生成的各类Input框添加 class ": "form-control"样式'''
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),
        # }

    '''方法二：改源码，通过循环找到所有的插件，设置插件的属性field.widget.attrs = class ": "form-control" '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到每个字段对象的插件field.widget.attrs，添加class="form-control"
        # 对象 field
        for name, field in self.fields.items():
            # 设置password不应用 class="form-control"效果
            # if name == "password":
            #     continue
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def user_model_form_add(request):
    """ 添加用户（ModelForm版本）"""
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {"form": form})

    # 用户POST提交数据，数据校验。
    if request.method == "POST":
        form = UserModelForm(data=request.POST)
        if form.is_valid():
            # 如果数据合法，保存到数据库
            # {'name': '123', 'password': '123', 'age': 11, 'account': Decimal('0'), 'create_time': datetime.datetime(2011, 11, 11, 0, 0, tzinfo=<UTC>), 'gender': 1, 'depart': <Department: IT运维部门>}
            # print(form.cleaned_data)
            # models.UserInfo.objects.create(..)
            form.save()
            return redirect('/user/list/')

        # 校验失败（在页面上显示错误信息）
        else:
            return render(request, 'user_model_form_add.html', {"form": form})


def user_edit(request, nid):
    # 根据主键nid查找到要修改的那条记录
    """这里get()一定要写 pk=xxxx 否则报错"""
    instance = models.UserInfo.objects.get(pk=nid)
    # 或用filter实现
    # instance = models.UserInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        form = UserModelForm(instance=instance)
        return render(request, 'user_edit.html', {"form": form})

    # 用户POST提交数据，数据校验。
    if request.method == "POST":

        form = UserModelForm(data=request.POST, instance=instance)
        if form.is_valid():
            # print("cleaned_data:", form.cleaned_data)
            # print("changed_data:", form.changed_data)

            # 默认保存的是用户输入的所有数据，如果想要再用户输入以外增加一点值
            # form.instance.字段名 = 值
            form.save()
            return redirect('/user/list/')
        # 校验失败（在页面上显示错误信息）
        else:
            return render(request, "user_edit.html", {"form": form})


class PrettyModelForm(forms.ModelForm):
    # 验证：方式1 字段+正则
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )

    # 验证：方式2 钩子方法, ModelForm会自动调用函数名为 clean_字段名，在函数体内自己写验证方法
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]

        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")

        # 验证通过，用户输入的值返回
        return txt_mobile

    # 设置字段灰显，不可编辑
    level = forms.IntegerField(label="级别", disabled=True)

    class Meta:
        model = models.PrettyNum
        # fields = ["mobile", "price", "level", "status"]
        # exclude = ["level"]
        fields = "__all__"

    '''方法二：改源码，通过循环找到所有的插件，设置插件的属性field.widget.attrs = class ": "form-control" '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到每个字段对象的插件field.widget.attrs，添加class="form-control"
        # 对象 field
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


"""由于编辑和新增时业务逻辑不一样 需要分开写一个类来定义规则"""
"""添加：【正则表达式】【手机号不能存在】"""
"""编辑：【正则表达式】【除了自己以外，手机号不能存在】"""


class PrettyEditModelForm(forms.ModelForm):
    # 验证：方式1 字段+正则
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )

    # 验证：方式2 钩子方法, ModelForm会自动调用函数名为 clean_字段名，在函数体内自己写验证方法
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        # 获取当前编辑的哪一行的ID
        nid = self.instance.pk
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exclude(pk=nid).exists()
        if exists:
            raise ValidationError("手机号已存在")

        # 验证通过，用户输入的值返回
        return txt_mobile

    # 设置字段灰显，不可编辑
    level = forms.IntegerField(label="级别", disabled=True)

    class Meta:
        model = models.PrettyNum
        # fields = ["mobile", "price", "level", "status"]
        # exclude = ["level"]
        fields = "__all__"

    '''方法二：改源码，通过循环找到所有的插件，设置插件的属性field.widget.attrs = class ": "form-control" '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到每个字段对象的插件field.widget.attrs，添加class="form-control"
        # 对象 field
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def pretty_list(request):
    """ 靓号列表 """

    # select * from app02_prettynum order by id , level desc;
    queryset = models.PrettyNum.objects.all().order_by("id", "-level")
    return render(request, "pretty_list.html", {'queryset': queryset})


def pretty_add(request):
    """ 添加靓号 """
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, 'pretty_add.html', {"form": form})

    if request.method == "POST":
        form = PrettyModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/pretty/list/')
        else:
            return render(request, 'pretty_add.html', {"form": form})


def pretty_init_add(request):
    """ 添加靓号（一键添加） """

    # 创建初始测试数据
    init_pretty_list = [
        ("18468033999", 45, 2, 1),
        ("13077241792", 2, 1, 1),
        ("13077241795", 23, 2, 0),
        ("17880739082", 444, 3, 1),
        ("17727969245", 213123, 4, 0),
        ("17727969254", 9999999, 4, 0),
    ]
    # 添加到数据库中
    for data in init_pretty_list:
        # 解包数据
        mobile, price, level, status = data
        models.PrettyNum.objects.create(mobile=mobile, price=price, level=level, status=status)

    # 返回到用户列表页面
    return redirect("/pretty/list/")


def pretty_edit(request, nid):
    """ 编辑靓号 """
    row_object = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_object)
        return render(request, 'pretty_edit.html', {"form": form})

    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')

    return render(request, 'pretty_edit.html', {"form": form})


def pretty_delete(request):
    """ 删除靓号"""
    nid = request.GET.get('nid')

    # 删除
    models.PrettyNum.objects.filter(id=nid).delete()

    # 重定向回靓号列表
    return redirect("/pretty/list/")
