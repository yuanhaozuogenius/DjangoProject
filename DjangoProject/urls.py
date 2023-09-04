"""
URL configuration for DjangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

# from blog import views
# from app01 import views
from app02 import views

urlpatterns = [
    # blog
    # path('', views.home, name='home'),
    # path('post/<int:post_id>', views.post_detail, name='post_detail'),

    # app01
    # path('index/', views.index),
    # path('admin/', admin.site.urls),
    # path('news/', views.news),
    # path('news_unicom/', views.news_unicom),
    # path('login/', views.login),
    # path('info/list/', views.info_list),
    # path('info/add/', views.info_add),
    # path('info/delete/', views.info_delete),

    # app02 部门管理
    path('depart/list/', views.depart_list),
    path('depart/add/', views.depart_add),
    path('depart/delete/', views.depart_delete),
    path('depart/<int:nid>/edit/', views.depart_edit),

    path('user/list/', views.user_list),
    path('user/add/', views.user_add),
    path('user/model/form/add/', views.user_model_form_add),
    path('user/init_add/', views.user_init_add),
    path('user/delete/', views.user_delete),
    path('user/<int:nid>/edit/', views.user_edit),
]
