from tokenize import Comment
from django.shortcuts import get_object_or_404, redirect, render
from .forms import BlogForm, ProfileForm, UserUpdateForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, EmptyPage
from .models import Blogs, Author, Comment
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    blogs_author = Author.objects.all() 

    query = request.GET.get('query', "").strip()  
    blog_list = Blogs.objects.filter(title__icontains=query) if query else Blogs.objects.all()

    paginator = Paginator(blog_list, 3)  
    page_number = request.GET.get('page', 1)

    try:
        blogs = paginator.page(page_number)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES) 
        if form.is_valid():
            blog = form.save(commit=False) 
            author, created = Author.objects.get_or_create(user=request.user, defaults={"name": request.user.username})
            blog.save() 
            blog.authors.add(author)
            return redirect('home')
    else:
        form = BlogForm()

    context = {
        "blogs": blogs,
        "blogs_author": blogs_author,  
        "page_range": paginator.page_range,
        "form": form,  
    }

    return render(request, 'blogs/home.html', context)

def add_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES) 
        if form.is_valid():
            blog = form.save(commit=False) 
            
            author, created = Author.objects.get_or_create(user=request.user, defaults={"name": request.user.username})
            blog.save() 
            blog.authors.add(author)
            return redirect('home')
    else:
        form = BlogForm()
        
    return render(request, 'blogs/add_blog.html', {'form': form})


def blog_details(request, id):
    blog = get_object_or_404(Blogs, id=id)
    blog_comments = blog.comment_set.all()
    is_author = request.user.is_authenticated and blog.authors.filter(user=request.user).exists()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.info(request, 'You need to log in to post a comment.')
            return redirect('login')
        
        author, created = Author.objects.get_or_create(user=request.user, defaults={"name": request.user.username})
        comment_body = request.POST.get('body')  
        if comment_body:
            Comment.objects.create(
                user=author,
                blogs=blog,
                body=comment_body
            )
            return redirect('blog_detail', id=blog.id) 
    
    return render(request, 'blogs/blog_detail.html', {
        'blog': blog,
        'blog_comments': blog_comments,
        'is_author': is_author
    })




@login_required
def update_blog(request, id):
    blog = get_object_or_404(Blogs, id=id)
    if not blog.authors.filter(user=request.user).exists():
        messages.error(request, "You do not have permission to update this blog.")
        return redirect('blog_detail', id=blog.id)
    
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog updated successfully.")
            return redirect('blog_detail', id=blog.id)
    else:
        form = BlogForm(instance=blog)
    
    return render(request, 'blogs/update_blog.html', {'form': form, 'blog': blog})


@login_required
def delete_blog(request, id):
    blog = get_object_or_404(Blogs, id=id)
    if not blog.authors.filter(user=request.user).exists():
        messages.error(request, "You do not have permission to delete this blog.")
        return redirect('blog_detail', id=blog.id)
    
    if request.method == 'POST':
        blog.delete()
        messages.success(request, "Blog deleted successfully.")
        return redirect('blog_list')
    
    return render(request, 'blogs/confirm_delete_blog.html', {'blog': blog})




def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.user.user:
        messages.error(request, "You are not authorized to delete this comment.")
        return redirect('home')  
    comment.delete()
    messages.success(request, "Comment deleted successfully.")
    return redirect('home')  



@login_required(login_url='/login/')
def delete_blog(request, id):
    blog = get_object_or_404(Blogs, id=id)
    
    user = request.user
    if request.method == 'POST':
        blog.delete()  
        return redirect('home')  
    
    return render(request, "blogs/delete_blog.html", {'blog': blog, "user": user})


def author_profile(request, id):
    author = get_object_or_404(Author, id=id)
    blogs_by_author = Blogs.objects.filter(authors=author)

    context = {
        'author': author,
        'blogs_by_author': blogs_by_author
    }
    return render(request, 'blogs/author_profile.html', context)


@login_required
def profile(request):
    author = get_object_or_404(Author, user=request.user)
    blogs = Blogs.objects.filter(authors=author)
    user_form = UserUpdateForm(request.POST, instance=request.user)
    profile_form = ProfileForm(request.POST, request.FILES, instance=author)

    return render(request, 'blogs/profile.html', {
        'author': author,
        'blogs': blogs,
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def update_profile(request):
    author = get_object_or_404(Author, user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=author)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save() 
            profile_form.save()  
            return redirect('profile')  
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=author)
        
    return render(request, 'blogs/update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id)

    if request.user != comment.user.user:
        messages.error(request, "You do not have permission to delete this comment.")
        return redirect('blog_detail', id=comment.blogs.id)
    
    if request.method == 'POST':
        blog_id = comment.blogs.id
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
        return redirect('blog_detail', id=blog_id)

    return render(request, 'blogs/confirm_delete_comment.html', {'comment': comment})