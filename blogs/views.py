from tokenize import Comment
from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from .models import Books
from .forms import BookForm, BookUpdateForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, EmptyPage
from .models import Books, Author, Comment
from .forms import BookForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    blogs_author = Author.objects.all() 

    query = request.GET.get('query', "").strip()  
    books_list = Books.objects.filter(title__icontains=query) if query else Books.objects.all()

    paginator = Paginator(books_list, 3)  
    page_number = request.GET.get('page', 1)

    try:
        books = paginator.page(page_number)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)


    context = {
        "books": books,
        "blogs_author": blogs_author,  
        "page_range": paginator.page_range  
    }

    return render(request, 'blogs/home.html', context)

def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES) 
        if form.is_valid():
            book = form.save(commit=False) 
            
            author, created = Author.objects.get_or_create(user=request.user, defaults={"name": request.user.username})
            book.save() 
            book.authors.add(author)
            return redirect('home')
    else:
        form = BookForm()
        
    return render(request, 'blogs/add_book.html', {'form': form})


def blog_details(request, id):
    blog = get_object_or_404(Books, id=id)
    blog_comments = blog.comment_set.all()
    
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
        'blog_comments': blog_comments
    })




def delete_book(request, id):
    book = Books.objects.get(id=id)

    if request.method == 'POST':
        book.delete()

        return redirect('home')
    return render(request, "blogs/delete_book.html", {'book' : book})


def update_book(request, id):
    book = get_object_or_404(Books, id=id)
    book_form = BookUpdateForm(instance=book)

    if request.method == "POST":
        book_form = BookUpdateForm(request.POST, instance=book)

        if book_form.is_valid():
            book_form.save()
            return redirect('book_detail', id=id)  
        
    return render(request, 'blogs/update_book.html', {
        'book_form': book_form,
        'blogs': book
    })



@login_required(login_url='/login/')
def profile(request, id):
    author = Author.objects.get(id=int(id))
    headline= "My Blogs"
    context = {"author": author, "headline": headline}
    return render(request, "blogs/profile.html", context)


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
    blog = get_object_or_404(Books, id=id)
    
    user = request.user
    if request.method == 'POST':
        blog.delete()  
        return redirect('home')  
    
    return render(request, "blogs/delete_blog.html", {'blog': blog, "user": user})


def author_profile(request, id):
    author = get_object_or_404(Author, id=id)
    blogs_by_author = Books.objects.filter(authors=author)

    context = {
        'author': author,
        'blogs_by_author': blogs_by_author
    }
    return render(request, 'blogs/author_profile.html', context)