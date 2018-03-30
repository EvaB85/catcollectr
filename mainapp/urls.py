from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:cat_id>/', views.show, name='show'),
    path('post_cat/', views.post_cat, name='post_cat'),
    path('user/<username>', views.profile, name='profile'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup, name="signup"),
]
