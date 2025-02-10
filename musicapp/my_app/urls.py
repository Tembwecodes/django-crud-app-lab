from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('songs/', views.song_index, name='song_index'),
    path('songs/<int:pk>/', views.song_detail, name='song_detail'),
    path('songs/new/', views.song_create, name='song_create'),
    path('songs/<int:pk>/edit/', views.song_update, name='song_update'),
    path('songs/<int:pk>/delete/', views.song_delete, name='song_delete'),

      # New Review URLs
    path('songs/<int:song_pk>/reviews/new/', views.review_create, name='review_create'),
    path('reviews/<int:pk>/edit/', views.review_update, name='review_update'),
    path('reviews/<int:pk>/delete/', views.review_delete, name='review_delete'),

    # signup route
     path('accounts/signup/', views.signup, name='signup'),

     # playlist routes
    path('playlists/', views.playlist_index, name='playlist_index'),
    path('playlists/<int:pk>/', views.playlist_detail, name='playlist_detail'),
    path('playlists/new/', views.playlist_create, name='playlist_create'),
    path('playlists/<int:pk>/edit/', views.playlist_update, name='playlist_update'),
    path('playlists/<int:pk>/delete/', views.playlist_delete, name='playlist_delete'),
    path('playlists/<int:playlist_pk>/add/<int:song_pk>/', views.add_to_playlist, name='add_to_playlist'),
    path('playlists/<int:playlist_pk>/remove/<int:song_pk>/', views.remove_from_playlist, name='remove_from_playlist'),
]
