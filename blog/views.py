import os
import urllib.request
from google_images_search import GoogleImagesSearch
from django.http import HttpResponseRedirect
from django.core.files import File
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from .models import Post, BookCover
from local_settings import API_KEY, CX
import hashlib

gis = GoogleImagesSearch(API_KEY, CX)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        posts = Post.objects.filter(public=True).order_by('-date') 
        query = self.request.GET.get('search')
        if query:
            posts = posts.filter(bookTitle__icontains=query)          
        return posts


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        posts =  Post.objects.filter(author=user).order_by('-date')
        if self.request.user != user:
            posts = posts.filter(public=True).order_by('-date')
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author"] = get_object_or_404(User, username=self.kwargs.get('username'))
        context["display_post_control_buttons"] = True
        return context
    

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        other = Post.objects.filter(bookTitle__icontains=self.object.bookTitle)
        other = other.filter(public=True).order_by('-date')
        context["other_posts"] = other
        context["display_post_control_buttons"] = True
        context["display_book_cover"] = True
        return context

class SaveBookCoverMixin:
    IMG_TYPE = "photo"
    NUM_OF_RESULTS = 1

    def find_cover_url(self,book_title):
        search_params = {
            'q': book_title + ' book cover',
            'num': self.NUM_OF_RESULTS,
            'imgType': self.IMG_TYPE
        }
        gis.search(search_params=search_params)
        return gis.results()[0].url
        
    def image_from_url(self, url, filename):
        # Specify the request header to avoid 403 error
        # https://stackoverflow.com/questions/34957748/http-error-403-forbidden-with-urlretrieve
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, "media/"+filename)

    def save_cover(self, url, post):
        hash = int(hashlib.sha1(url.encode("utf-8")).hexdigest(), 16) % (10 ** 8)
        filename = "book_covers/" + str(hash) + ".jpg"
        sameBookCovers = BookCover.objects.filter(image= filename)
        if (sameBookCovers.count() > 0):
            cover = BookCover(post = post, image = sameBookCovers.first().image)
        else:
            self.image_from_url(url, filename)
            cover = BookCover(post = post, image = filename)
        cover.save()

class PostCreateView(LoginRequiredMixin, CreateView, SaveBookCoverMixin):
    model = Post
    fields = ['bookTitle', 'bookAuthor', 'review', 'public']

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()
        url = self.find_cover_url(form.cleaned_data['bookTitle'])
        self.save_cover(url, self.object)
        
        return HttpResponseRedirect(self.get_success_url())

class IsUserAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostUpdateView(LoginRequiredMixin, IsUserAuthorMixin, UpdateView):
    model = Post
    fields = ['bookTitle', 'bookAuthor', 'review', 'public']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, IsUserAuthorMixin, DeleteView):
    model = Post
    success_url = '/'

def about(request):
    return render(request, 'blog/about.html')