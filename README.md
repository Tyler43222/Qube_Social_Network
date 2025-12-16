Project demo video: https://youtu.be/qWUINlKI_-s

My project, Qube, is a social network site modelled off x.com. My goal was to build a site with all of the core features from present day social network sites. 

On the main home page, users can make posts using the text, image upload, and select category fields. Under that they can scroll the main feed, liking/unliking posts as they choose. Clicking any of the eight categories at the top of the page with load only posts who are in that category as specified by the post creator. Users can also search for users or posts under the search tab, or look at posts from the people they follow. If a user clicks on a post, they are brought to a detailed view of the post where users can view and make their own comments. Users an also see detailed profile data for any user by clicking a users username or profile photo on a post. This data includes the number of followers/following, a biography, and all posts from that user. The main home feed, category feed, search feed, and following feed all implement a post sorting algorithm that takes into account the number of likes, number of comments, how recently it was posted, and how long user spend looking at the post to determine how high each post ranks on the feed. Post with a high amount of each of these four factors will rank higher than those without. Comments also use a more basic sorting algorithm that uses like count and recency.

Models:
    User (following, liked posts/comments, profile_photo, biography), Post (content, image, category), Comment, PostEngagement (page_rank, engagement_time), CommentEngagement (comment_rank)

Views:
    algorithm.py: 
        Implements the sorting algorithm for posts and comments. For posts, the pagerank function assigns a numerical page rank value to each post with the following weights: Recency: 30%, like count: 20%, comment count: 30%, and cumulative time engagement: 20%. Recency is determined by calculating the amount of hours since the post was posted, and cumulative time engagement is calculated by adding total amount of time users have spend of the post details page of a given post. Posts with higher time engagement means the post is more intersting to users and should rank higher(engagement.js tracks time elapsed and sends data to algorithm.py).
        For comments, the commentrank function also assigns a numerical page rank value to each comment with the following weights: Recency: 40%, like count: 60%,
    auth.py: 
        Login, register, and logout functions.
    posts.py:
        Renders feeds (home, search, categories, following, profile) and handles CRUD for posts and comments. Renders detailed post view.
    users.py:
        Renders the page where users can edit their profile photo and biography and handles CRUD for the user model.
    utils.py:
        Handles pagination for infinite scroll, timestamp formatting, like toggling, and sessions so non-authenticated users can like posts and comments.

JS:
    edit.js:
        Functions for users to edit their own posts and profiles.
    engagement.js:
        Tracks how long users spend on posts
    main.js:
        Initialize posts and infinite scroll
    utils.js:
        Handles infinite scroll, like actions, and helper functions for edit.js

HTML:
    layout.html:
        Base layout with the bootstrap sidebar.
    index.html:
        Renders the post composer, categories, all feeds, and the profile area.
    post_details.html:
        Renders the post details view with comments and comment composer. 
    partials:
        Renders all the buttons on a post including like, comment, and edit buttons.


## Database
Currently using SQLite for easy development/demo. 

**Production-ready**: To switch to PostgreSQL, update settings.py:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # configuration details ...
    }
}

