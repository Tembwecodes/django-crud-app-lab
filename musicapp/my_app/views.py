from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Song, Review, Playlist
from .forms import SongForm, ReviewForm, PlaylistForm

def home(request):
    return render(request, 'home.html')

def song_index(request):
    songs = Song.objects.all()
    return render(request, 'songs/index.html', {'songs': songs})

def song_detail(request, pk):
    song = get_object_or_404(Song, pk=pk)
    return render(request, 'songs/detail.html', {'song': song})

@login_required
def song_create(request):
    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            song = form.save(commit=False)
            song.user = request.user
            song.save()
            return redirect('song_detail', pk=song.pk)
    else:
        form = SongForm()
    return render(request, 'songs/form.html', {'form': form, 'type': 'Create'})

@login_required
def song_update(request, pk):
    song = get_object_or_404(Song, pk=pk)
    if song.user != request.user:
        return redirect('song_detail', pk=pk)
    if request.method == 'POST':
        form = SongForm(request.POST, instance=song)
        if form.is_valid():
            song = form.save()
            return redirect('song_detail', pk=song.pk)
    else:
        form = SongForm(instance=song)
    return render(request, 'songs/form.html', {'form': form, 'type': 'Update'})

@login_required
def song_delete(request, pk):
    song = get_object_or_404(Song, pk=pk)
    if song.user != request.user:
        return redirect('song_detail', pk=pk)
    if request.method == 'POST':
        song.delete()
        return redirect('song_index')
    return render(request, 'songs/confirm_delete.html', {'song': song})

@login_required
def review_create(request, song_pk):
    song = get_object_or_404(Song, pk=song_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.song = song
            review.user = request.user
            review.save()
            return redirect('song_detail', pk=song_pk)
    else:
        form = ReviewForm()
    return render(request, 'reviews/form.html', {
        'form': form, 
        'song': song,
        'type': 'Create'
    })

@login_required
def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.user != request.user:
        return redirect('song_detail', pk=review.song.pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('song_detail', pk=review.song.pk)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'reviews/form.html', {
        'form': form,
        'review': review,
        'type': 'Update'
    })

@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.user != request.user:
        return redirect('song_detail', pk=review.song.pk)
    song_pk = review.song.pk
    if request.method == 'POST':
        review.delete()
        return redirect('song_detail', pk=song_pk)
    return render(request, 'reviews/confirm_delete.html', {'review': review})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# New Playlist views
@login_required
def playlist_index(request):
    playlists = Playlist.objects.filter(user=request.user)
    return render(request, 'playlists/index.html', {'playlists': playlists})

@login_required
def playlist_detail(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk)
    return render(request, 'playlists/detail.html', {'playlist': playlist})

@login_required
def playlist_create(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.user = request.user
            playlist.save()
            form.save_m2m()  # Needed for many-to-many relationships
            return redirect('playlist_detail', pk=playlist.pk)
    else:
        form = PlaylistForm()
    return render(request, 'playlists/form.html', {'form': form, 'type': 'Create'})

@login_required
def playlist_update(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk)
    if playlist.user != request.user:
        return redirect('playlist_index')
    if request.method == 'POST':
        form = PlaylistForm(request.POST, instance=playlist)
        if form.is_valid():
            form.save()
            return redirect('playlist_detail', pk=playlist.pk)
    else:
        form = PlaylistForm(instance=playlist)
    return render(request, 'playlists/form.html', {'form': form, 'type': 'Update'})

@login_required
def playlist_delete(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk)
    if playlist.user != request.user:
        return redirect('playlist_index')
    if request.method == 'POST':
        playlist.delete()
        return redirect('playlist_index')
    return render(request, 'playlists/confirm_delete.html', {'playlist': playlist})

@login_required
def add_to_playlist(request, playlist_pk, song_pk):
    playlist = get_object_or_404(Playlist, pk=playlist_pk, user=request.user)
    song = get_object_or_404(Song, pk=song_pk)
    playlist.songs.add(song)
    return redirect('playlist_detail', pk=playlist_pk)

@login_required
def remove_from_playlist(request, playlist_pk, song_pk):
    playlist = get_object_or_404(Playlist, pk=playlist_pk, user=request.user)
    song = get_object_or_404(Song, pk=song_pk)
    playlist.songs.remove(song)
    return redirect('playlist_detail', pk=playlist_pk)