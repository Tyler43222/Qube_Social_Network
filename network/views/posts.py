from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from ..models import User, Post, Comment
from .utils import format_timestamp, is_liked, categories, toggle_like_helper, preparePosts
from .algorithm import pagerank, commentrank

def index(request):
    pagerank()
    post_list = Post.objects.all().order_by('-engagement__page_rank')
    # Calculate time display for each post
    posts = preparePosts(request, post_list)

    return render(request, "network/index.html", {
        "posts": posts,
        "create_field": True,
        "show_categories": True,
        "categories": categories
        })

@login_required
def create_post(request): 
    if request.method == "POST":
        Post.objects.create(
            creator = request.user,
            content = request.POST.get("post-content"),
            image = request.FILES.get("post-image"),
            category = request.POST.get("category")
        )
    return HttpResponseRedirect(reverse("index"))

@login_required
def create_comment(request, post_id):
    if request.method == "POST":
        Comment.objects.create(
            post = get_object_or_404(Post, id=post_id),
            commenter = request.user,
            comment = request.POST.get("comment-content")
        )
    return HttpResponseRedirect(reverse("post_details", args=[post_id]))

def profile_view(request, username):
    target_user = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(creator=target_user).order_by('-timestamp')
    posts = preparePosts(request, post_list)

    return render(request, "network/index.html", {
        "profile_user": target_user,
        "posts": posts,
        "header": True,
        "current_user": request.user.is_authenticated and request.user == target_user,
        "is_following": request.user.is_authenticated and request.user.following.filter(username=target_user.username).exists(),
        "followers_count": target_user.followers.count(),
        "following_count": target_user.following.count()
        })

@login_required
def following_view(request):
    # Load posts from users the current user is following
    users = request.user.following.all()
    post_list = Post.objects.filter(creator__in=users).order_by('-engagement__page_rank')
    empty_following = False
    if not post_list:
        empty_following = True
    posts = preparePosts(request, post_list)

    return render(request, "network/index.html", {
        "posts": posts,
        "following_view": True,
        "empty_following": empty_following
        })

@login_required
def update_post(request, post_id):
    # Updates post content in database to user edit
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        if post.creator != request.user:
            return JsonResponse({"error": "Cannot edit post"})
        
        post.content = request.POST.get("content", post.content)
        if 'image' in request.FILES:
            # Delete old image if it exists
            if post.image:
                post.image.delete(save=False)
            post.image = request.FILES['image']
        post.save()
        
        image_url = post.image.url if post.image else None
        return JsonResponse({"success": True, "content": post.content, "image_url": image_url})
    return JsonResponse({"error": "POST is needed"})

def toggle_like(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        return toggle_like_helper(request, post, post_id, 'liked_posts')
    return JsonResponse({"error": "POST required"})

def toggle_comment_like(request, comment_id):
    if request.method == "POST":
        comment = get_object_or_404(Comment, id=comment_id)
        return toggle_like_helper(request, comment, comment_id, 'liked_comments')
    return JsonResponse({"error": "POST required"})

def post_details(request, post_id):
    commentrank()
    post = get_object_or_404(Post, id=post_id)
    format_timestamp(post)
    is_liked(request, post)
    comment_list = post.comments.all().order_by('-engagement__comment_rank')
    comments = preparePosts(request, comment_list)
    
    return render(request, "network/post_details.html", {
        "post": post,
        "comments": comments
        })

@login_required
def delete_post(request, post_id):
    if request.method == "DELETE":
        post = get_object_or_404(Post, id=post_id)
        if post.creator != request.user:
            return JsonResponse({"success": False, "error": "Permission denied"})
        # Delete the image file from filesystem before deleting the post
        if post.image:
            post.image.delete(save=False)
        post.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "DELETE required"})

def search(request):
    empty = False
    query = request.GET.get("q", "").strip()
    if query:
        post_list = (
            Post.objects.filter(content__icontains=query) |
            Post.objects.filter(creator__username__icontains=query)
        ).distinct().order_by('-engagement__page_rank')
        if not post_list:
            empty = True
    else:
        post_list = Post.objects.all().order_by('-engagement__page_rank')
        
    posts = preparePosts(request, post_list)

    return render(request, "network/index.html", {
        "posts": posts,
        "can_search": True,
        "search_query": query,
        "empty": empty
        })

def category_view(request, category):
    post_list = Post.objects.filter(category=category).order_by('-engagement__page_rank')
    posts = preparePosts(request, post_list)
    
    return render(request, "network/index.html", {
        "posts": posts,
        "create_field": True,
        "show_categories": True,
        "categories": categories,
        "active_category": category
        })