from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils import timezone
from ..models import User, Post, Comment

categories = ["news", "tech", "entertainment", "health", "nature", "sports", "education", "humor"]

def paginate(request, queryset):
    page_number = request.GET.get("page", 1)
    paginator = Paginator(queryset, 10)
    return paginator.get_page(page_number)

def is_liked(request, post):
    session = 'liked_comments' if isinstance(post, Comment) else 'liked_posts'
    
    if request.user.is_authenticated:
        liked = request.user.liked_comments.all() if isinstance(post, Comment) else request.user.liked_posts.all()
        post.is_liked_by_user = post in liked
    else:
        post.is_liked_by_user = post.id in request.session.get(session, [])

def format_timestamp(post):
    # Sets time atributes for better formatting of displayed time
    hours_ago = (timezone.now() - post.timestamp).total_seconds() / 3600
    local_time = timezone.localtime(post.timestamp)
    if hours_ago < 24:
        post.time_display = f"{int(hours_ago)}h"
    else:
        post.time_display = local_time.strftime("%b %d, %Y")
    post.time_detail = local_time.strftime("%I:%M%p · %b %d, %Y")

@login_required
def toggle_follow(request, username):
    target_user = get_object_or_404(User, username=username)
    if target_user != request.user: 
        if "unfollow" in request.POST:
            request.user.following.remove(target_user)
        elif "follow" in request.POST:
            request.user.following.add(target_user)
    return HttpResponseRedirect(reverse("profile", args=[username]))

def toggle_like_helper(request, obj, obj_id, type):
    if request.user.is_authenticated:
        user_likes = getattr(request.user, type)
        if user_likes.filter(id=obj_id).exists():
            user_likes.remove(obj)
            liked = False
        else:
            user_likes.add(obj)
            liked = True
    else:
        liked_items = [int(x) for x in request.session.get(type, [])]
        if obj_id in liked_items:
            liked_items.remove(obj_id)
            liked = False
        else:
            liked_items.append(obj_id)
            liked = True
        request.session[type] = liked_items
        request.session.modified = True
    
    like_field = 'liked' if isinstance(obj, Post) else 'liked_comment'
    likes_count = getattr(obj, like_field).count()
    if not request.user.is_authenticated and liked:
        likes_count += 1
    
    return JsonResponse({"success": True, "liked": liked, "likes_count": likes_count})

def init_session_likes(request):
    # Uses sessions to track likes from unauthenticated users
    if 'liked_posts' not in request.session:
        request.session['liked_posts'] = []
    if 'liked_comments' not in request.session:
        request.session['liked_comments'] = []

def preparePosts(request, queryset):
    init_session_likes(request)
    for obj in queryset: 
        format_timestamp(obj)
        is_liked(request, obj)
    posts = paginate(request, queryset)
    return posts