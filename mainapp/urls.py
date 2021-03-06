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
    path('like_cat/', views.like_cat, name="like_cat"),
    path('<int:cat_id>/edit', views.edit_cat, name="edit_cat"),
    path('<int:cat_id>/destroy/', views.delete_cat, name="delete_cat"),
]
