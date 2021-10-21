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
from .models import Post

def home(request):
    context = {
        'posts': Post.objects.all(),
    }
    return render(request, 'blog/home.html', context)

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
        return context
    

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        other = Post.objects.filter(bookTitle__icontains=self.object.bookTitle).order_by('-date')
        context["otherPosts"] = other
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['bookTitle', 'bookAuthor', 'review', 'public']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['bookTitle', 'bookAuthor', 'review', 'public']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html')