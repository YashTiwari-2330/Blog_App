from django.shortcuts import render
from .models import Post
from .forms import PostForm , UserRegistrationForm , User
from django.shortcuts import get_object_or_404, redirect , HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q

# Create your views here.

def index(request):
    return render(request , "index.html")

def post_list(request):
    try:
        posts = Post.objects.filter(status = 'published').order_by('-created_at')

    except Post.DoesNotExist:
        posts = None

    return render(request, 'post_list.html', {'posts': posts})

@login_required
def post_draft_list(request):
    drafts = Post.objects.filter(status='draft', author=request.user).order_by('-created_at')
    return render(request, 'post_draft_list.html', {'drafts': drafts})


@login_required
def post_publish(request, id):
    post = get_object_or_404(Post, pk=id, author=request.user, status='draft')
    post.status = 'published'
    post.save()
    return redirect('post_list')

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
         form = PostForm()
    return render(request, 'post_create.html', {'form': form})

@login_required
def post_edit(request , id):
    post = get_object_or_404(Post , pk=id , author = request.user)
    if request.method == "POST":
        form = PostForm(request.POST , request.FILES , instance = post)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.save()
            # Send drafts to drafts page, published to home
            return redirect('post_draft_list' if post.status == 'draft' else 'post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form, 'post': post})

@login_required
def post_delete(request , id):
    post = get_object_or_404(Post , pk=id , author=request.user)
    if request.method == "POST":
        post.delete()
        return redirect('post_list')
    return render(request, 'post_delete.html', {'post': post})

def register(request):
    form = None
    if request.method == "POST":
       form = UserRegistrationForm(request.POST)
       if form.is_valid():
          user = form.save(commit=False)
          user.set_password(form.cleaned_data['password1'])
          user.save()
          login(request, user)
          return redirect('post_list')
    else:
        form = UserRegistrationForm()

    return render(request , "registration/register.html" , {'form':form})

@login_required
def search_post(request):
    query = request.GET.get("query") # search input from navbar
    posts = Post.objects.filter(title__icontains=query)  # only published posts
    return render(request , "search_post.html" , {"posts":posts , "query" : query})