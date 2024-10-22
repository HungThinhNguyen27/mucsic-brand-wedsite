from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r"^$", views.index, name="index"),
    path("", views.songs, name="songs"),
    path("", views.photos, name="photos"),
    path("", views.login_view, name="login"),
    path("", views.logout_view, name="logout"),
    path("", views.signup, name="signup"),
    path("", views.concerts, name="concerts"),
    path("concert-detail/<int:id>", views.concert_detail, name="concert_detail"),
    path("concert_attendee/", views.concert_attendee, name="concert_attendee"),
    path("songs/", views.songs, name="songs"),
    path("photos/", views.photos, name="photos"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("concert/", views.concerts, name="concerts"),

]
