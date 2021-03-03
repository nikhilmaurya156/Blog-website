from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, AddingComment, PostDetail, Suggestion, Bookmark
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from PIL import Image
from django.contrib import messages
from django.utils.text import slugify
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context )

def likes(request, **kwargs):
    p = Post.objects.get(slug=kwargs['slug'])
    p.votes+=1
    p.save()
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context )


def bookmark(request, **kwargs):
    p = Post.objects.get(slug=kwargs['b_title'])
    u = User.objects.get(username=kwargs['b_author'])
    b,created = Bookmark.objects.get_or_create(b_author=u, b_title=p)
    b.save()
    if b.bookmark == False:
        b.bookmark=True
        b.save()
        messages.success(request, 'Bookmark Created')
        return redirect('blog_home')
    if b.bookmark == True:
        b.bookmark=False
        b.save()
        messages.success(request, 'Bookmark Removed')
        return redirect('blog_home')


def autocompleteModel(request):
    if 'term' in request.GET:
        search_qs = Post.objects.filter(title__icontains=request.GET.get('term'))
        results = []
        for r in search_qs:
            results.append(r.title)
        return JsonResponse(results, safe=False)
    else:
        print(request.POST)
        search_qs = Post.objects.filter(title__icontains=request.POST.get('your_name'))
        context = {'posts':search_qs, 'hii':'1'}
        return render(request, 'blog/home.html', context)
    return render(request, 'blog/home.html')


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2


class FieldPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2

    def get_queryset(self):
        return Post.objects.filter(field=self.kwargs.get('slug'))

def bookmarks(request):
    b=[]
    print(request.user)
    for i in Bookmark.objects.filter(b_author=request.user, bookmark='True'):
        b.append(i.b_title)
    print(b)
    context = {
        'posts': Post.objects.all(),
        'a': b
    }
    return render(request, 'blog/bookmark.html', context )


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('slug'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class SuggestionCreateView(LoginRequiredMixin, CreateView):
    model = Suggestion
    fields = ['suggest']

    def form_valid(self, form):
        form.instance.s_author = self.request.user
        return super().form_valid(form)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'field', 'about_blog','starting_image','image_description', 'main_content', 'about_you']

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostCreateAddView(LoginRequiredMixin, CreateView):
    model = PostDetail
    fields = ['topic_heading','image','content', 'url_title','urls_links']
    context_object_name = 'post'

    def form_valid(self, form):
        p = Post.objects.get(slug=self.kwargs.get('slug'))
        form.instance.p_title = p
        return super().form_valid(form)


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'


class PostUpdateView(LoginRequiredMixin, UpdateView, UserPassesTestMixin):
    model = Post
    fields = ['title', 'field', 'about_blog','starting_image','image_description', 'main_content',  'about_you']

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDetailUpdateView(LoginRequiredMixin, UpdateView, UserPassesTestMixin):
    model = PostDetail
    fields = ['topic_heading','image','content', 'urls']

    def form_valid(self, form):
        form.instance.p_title =Post.objects.get(slug=self.kwargs.get('slug'))
        return super().form_valid(form)

    def test_func(self):
        post = Post.objects.get(slug=self.kwargs.get('slug'))
        if self.request.user == post.author:
            return True
        return False

def updateForm(request, slug):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and u_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Account Has Been Updated')
            return redirect('profile')
    else:
        p = Post.objects.get(slug=slug)
        q = PostDetail.objects.filter(p_title=p.id)
        p_form = PostUpdateForm(instance=p)
        q_form = PostDUpdateForm(instance=q[0])
    context = {
        'p_form': p_form,
        'q_form': q_form,
    }
    return render(request, 'blog/post_update_form.html', context)
    

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


class PostDetailDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PostDetail
    success_url = '/'

    def test_func(self):
        post = Post.objects.get(slug=self.kwargs.get('slug'))
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


class PostComment(CreateView, LoginRequiredMixin):
    model = AddingComment
    template_name = 'blog/comment.html'
    fields = ['comment']

    def form_valid(self, form):
        form.instance.c_title = Post.objects.get(slug=self.kwargs.get('slug'))
        form.instance.C_author = self.request.user
        return super().form_valid(form)


class CommmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AddingComment


    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'slug': self.kwargs['slug']})
        
    def test_func(self):
        comm = AddingComment.objects.get(id=self.kwargs.get('pk'))
        if self.request.user == comm.C_author:
            return True
        return False


@login_required
def comment_detail(request, pk):
    context = {
        'post': Post.objects.filter(id=pk).first()
    }
    return render(request, 'blog/comment.html', context)


@login_required
def submit(request):
    pos = Post.objects.filter(id=pk).first()
    pos.addingcomment_set.create(comment=request.POST['com'], C_author=request.user)
    return redirect('blog_home')


