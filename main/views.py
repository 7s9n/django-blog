from django.shortcuts import render , get_object_or_404
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post
from django.contrib.auth.models import User
# Create your views here.

#dummy data
posts = [
    {
        'author':'Hussein Sarea',
        'title':'Blog post 1',
        'content':'First post content',
        'data_posted':'June 27 , 2021',
    },
    {
        'author':'Moataz Sarea',
        'title':'Blog post 2',
        'content':'Second post content',
        'data_posted':'June 27 , 2021',
    },
]
# def home(request):
#     context = {
#         'blog_posts': Post.objects.all(),
#         'title':'Recent blogs'
#     }
#     return render(request=request , template_name='main/home.html' , context=context)

def about(request):
    return render(request=request , template_name='main/about.html' , context={'title':'about'})

class PostListView(ListView):
    model = Post
    template_name = 'main/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'blog_posts' #by default it's object
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'main/user_posts.html'
    context_object_name = 'blog_posts' #by default it's object
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User , username=self.kwargs.get('username'))
        return Post.objects.filter(author = user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin , CreateView):
    model = Post
    fields = ['title' , 'content']

    def form_valid(self , form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_form(self):
        form = super(PostCreateView, self).get_form()
        form.fields['title'].widget.attrs = {
            'class':'form-control col-md-6',
            'placeholder':'Post\'s title',
        }
        form.fields['content'].widget.attrs = {
            'class':'form-control col-md-6',
            'placeholder':'Post\'s content',
        }
        return form

class PostUpdateView(UserPassesTestMixin,LoginRequiredMixin , UpdateView):
    model = Post
    fields = ['title' , 'content']

    def form_valid(self , form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_form(self):
        form = super(PostUpdateView, self).get_form()
        form.fields['title'].widget.attrs = {
            'class':'form-control col-md-6',
            'placeholder':'Post\'s title',
        }
        form.fields['content'].widget.attrs = {
            'class':'form-control col-md-6',
            'placeholder':'Post\'s content',
        }
        return form

    def test_func(self):
        post = self.get_object() #main.models.Post
        return self.request.user == post.author

class PostDeleteView(UserPassesTestMixin,LoginRequiredMixin , DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        # post = get_object_or_404(Post , pk=self.kwargs.get('pk'))
        post = self.get_object() #main.models.Post
        return self.request.user == post.author
