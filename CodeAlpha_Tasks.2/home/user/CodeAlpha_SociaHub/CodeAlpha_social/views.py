from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CommentForm, PostForm, ProfileForm, RegisterForm
from .models import Comment, Follow, Post, PostLike
from django.http import JsonResponse

def home(request):
    posts = Post.objects.select_related('author', 'author__profile').prefetch_related('comments__author', 'likes').annotate(
        likes_total=Count('likes'),
        comments_total=Count('comments')
    )
    post_form = PostForm()
    comment_form = CommentForm()

    liked_post_ids = set()
    following_ids = set()
    if request.user.is_authenticated:
        liked_post_ids = set(PostLike.objects.filter(user=request.user).values_list('post_id', flat=True))
        following_ids = set(Follow.objects.filter(follower=request.user).values_list('following_id', flat=True))

    context = {
        'posts': posts,
        'post_form': post_form,
        'comment_form': comment_form,
        'liked_post_ids': liked_post_ids,
        'following_ids': following_ids,
    }
    return render(request, 'social/home.html', context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome! Your account has been created.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = profile_user.posts.all().prefetch_related('comments__author', 'likes')
    is_following = False
    if request.user.is_authenticated and request.user != profile_user:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    return render(request, 'social/profile.html', {
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following,
        'comment_form': CommentForm(),
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
       form = ProfileForm(
       request.POST,
       request.FILES,
       instance=request.user.profile
       )
       if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'social/profile_edit.html', {'form': form})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(
        request.POST,
        request.FILES
        )
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully.')
    return redirect('home')


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(
        request.POST,
        request.FILES,
        instance=post
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully.')
            return redirect('profile', username=request.user.username)
    else:
        form = PostForm(instance=post)
    return render(request, 'social/post_form.html', {'form': form, 'title': 'Edit Post'})


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted.')
        return redirect('profile', username=request.user.username)
    return render(request, 'social/post_confirm_delete.html', {'post': post})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            comment = Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )

            return JsonResponse({
                "id": comment.id,
                "author": comment.author.username,
                "content": comment.content,
                "created_at": comment.created_at.strftime("%b %d, %Y • %H:%M")
            })

    return JsonResponse({"error": "Invalid request"}, status=400)
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author or request.user == comment.post.author:
        comment.delete()
        messages.success(request, 'Comment deleted.')
    else:
        messages.error(request, 'You do not have permission to delete this comment.')
    next_url = request.GET.get('next') or 'home'
    return redirect(next_url)


@login_required
def toggle_like(request, post_id):
    print("========== LIKE VIEW CALLED ==========")
    print("User:", request.user)
    print("Post ID:", post_id)

    post = get_object_or_404(Post, id=post_id)

    like, created = PostLike.objects.get_or_create(
        user=request.user,
        post=post
    )

    print("Created:", created)

    if created:
        liked = True
    else:
        like.delete()
        liked = False

    print("Total Likes:", post.likes.count())

    return JsonResponse({
        "likes": post.likes.count(),
        "liked": liked
    })
    
@login_required
def toggle_follow(request, username):
    target_user = get_object_or_404(User, username=username)
    if target_user == request.user:
        messages.warning(request, 'You cannot follow yourself.')
        return redirect('profile', username=username)

    follow, created = Follow.objects.get_or_create(follower=request.user, following=target_user)
    if not created:
        follow.delete()
        messages.info(request, f'You unfollowed {target_user.username}.')
    else:
        messages.success(request, f'You are now following {target_user.username}.')
    return redirect('profile', username=username)
