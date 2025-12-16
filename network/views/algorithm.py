from datetime import timezone, datetime
from django.http import HttpResponse
import json
from django.shortcuts import get_object_or_404
from ..models import Post, Comment, PostEngagement, CommentEngagement

def pagerank():
    # Assign a numerical page rank value to each post with the following weights: 
    # Recency: 30%, like count: 20%, comment count: 30%, and cumulative time engagement: 20%
    posts = Post.objects.all()
    post_data = []
    for post in posts:
        engagement, _ = PostEngagement.objects.get_or_create(post=post)
        hours_since_post = (datetime.now(timezone.utc) - post.timestamp).total_seconds() / 3600
        likes_count = post.liked.count()
        comments_count = post.comments.count()
        view_time = engagement.engagement_time
        post_data.append({'post': post, 'engagement': engagement, 'hours': hours_since_post, 'likes': likes_count, 'comments': comments_count, 'view_time': view_time})
    
    # Find max value of each metric for normalization
    max_hours = max([p['hours'] for p in post_data]) if post_data else 1
    max_likes = max([p['likes'] for p in post_data]) if post_data else 1
    max_comments = max([p['comments'] for p in post_data]) if post_data else 1
    max_view_time = max([p['view_time'] for p in post_data]) if post_data else 1

    for data in post_data:
        # # Calculate relative recency, like, comment, and engagement rank and apply weights
        time_score = (1 - (data['hours'] / max_hours)) * 30 if max_hours > 0 else 0
        likes_score = (data['likes'] / max_likes) * 20 if max_likes > 0 else 0
        comments_score = (data['comments'] / max_comments) * 30 if max_comments > 0 else 0
        engagement_score = (data['view_time'] / max_view_time) * 20 if max_view_time > 0 else 0

        # Assign page ranks
        data['engagement'].page_rank = time_score + likes_score + comments_score + engagement_score
        data['engagement'].save()

def commentrank():
    # Assign a numerical page rank value to each comment. 
    # Weighted so recency determines 40% of a comment's pagerank, like count determines 60%
    comments = Comment.objects.all()
    comment_data = []
    for comment in comments:
        engagement, _ = CommentEngagement.objects.get_or_create(comment=comment)
        hours_since_post = (datetime.now(timezone.utc) - comment.timestamp).total_seconds() / 3600
        likes_count = comment.liked_comment.count()
        comment_data.append({'comment': comment, 'engagement': engagement, 'hours': hours_since_post, 'likes': likes_count})

    # Find max value of each metric for normalization
    max_hours = max([c['hours'] for c in comment_data]) if comment_data else 1
    max_likes = max([c['likes'] for c in comment_data]) if comment_data else 1

    for data in comment_data:
        # Calculate relative recency and like rank and apply weights
        time_score = (1 - (data['hours'] / max_hours)) * 40 if max_hours > 0 else 0
        likes_score = (data['likes'] / max_likes) * 60 if max_likes > 0 else 0

        # Assign page ranks
        data['engagement'].comment_rank = time_score + likes_score
        data['engagement'].save()

def track_engagement(request, post_id):
    # Fetches elapsed time data and updates engagement model
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        data = json.loads(request.body)
        seconds = int(data.get("seconds", 0))
        
        engagement, _ = PostEngagement.objects.get_or_create(post=post)
        engagement.engagement_time += seconds
        engagement.save()
    return HttpResponse(status=204)