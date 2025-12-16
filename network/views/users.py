from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def user_profile(request):
    return render(request, "network/index.html", {
        "user_profile_view": True,
        "profile_user": request.user,
        "header": True,
        "current_user": True,
        "followers_count": request.user.followers.count(),
        "following_count": request.user.following.count()
        })

@login_required
def update_profile(request):
    if request.method == "POST":
        bio_text = request.POST.get("bio_text", "")
        
        request.user.biography = bio_text
        
        if 'profile_photo' in request.FILES:
            # Delete old profile photo if it exists
            if request.user.profile_photo:
                request.user.profile_photo.delete(save=False)
            request.user.profile_photo = request.FILES['profile_photo']
        
        request.user.save()
        
        photo_url = request.user.profile_photo.url if request.user.profile_photo else None
        return JsonResponse({"success": True, "photo_url": photo_url})
    return JsonResponse({"success": False})

@login_required
def delete_profile_photo(request):
    if request.method == "POST":
        if request.user.profile_photo:
            request.user.profile_photo.delete(save=True)
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})