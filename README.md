## Qube - Social Network

Qube is a social network web app modeled after X/Twitter.

### Tech stack
- Backend: Django function-based views, Django ORM
- Frontend: Django templates, ES module JavaScript, Bootstrap components
- Database: SQLite for development

### Features
- Create posts with text, an optional image upload, and an optional category.
- Browse feeds with infinite scroll:
  - Home feed (ranked)
  - Category feed (ranked)
  - Search feed (ranked)
  - Following feed (ranked)
  - User profile feed (reverse chronological)
- Like/unlike posts and comments (supports anonymous likes via session storage).
- Follow/unfollow users.
- Post detail view with ranked comments + time-on-post engagement tracking.
- Profile editing: upload/remove profile photo and add/edit biography.
- Mobile responsive design.

### How ranking works
This project computes a numeric rank and uses it for ordering:

- Posts: `PostEngagement.page_rank`
  - Weights: recency 30%, like count 20%, comment count 30%, time-on-post engagement 20%
  - Calculated in `network/views/algorithm.py::pagerank()`
  - Called on every request to the home feed (`network/views/posts.py::index()`), and saved to `PostEngagement`.

- Comments: `CommentEngagement.comment_rank`
  - Weights: recency 40%, like count 60%
  - Calculated in `network/views/algorithm.py::commentrank()`
  - Called when rendering the post detail page.

Time-on-post engagement:
- Once a user clicks on a post and the post detail page loads, the browser tracks how long they spend on that page before clicking off. 
- `network/static/network/engagement.js` periodically POSTs `{seconds: <elapsed>}` to `/post/<id>/track/`.
- The server endpoint `network/views/algorithm.py::track_engagement()` increments `PostEngagement.engagement_time`.

### Project structure
- `project/`: Django project settings + root URL config
- `network/`: single Django app
  - `models.py`: `User`, `Post`, `Comment`, `PostEngagement`, `CommentEngagement`
  - `views/`: `posts.py`, `auth.py`, `users.py`, `algorithm.py`, `utils.py`
  - `templates/network/`: server-rendered HTML (most routes render `index.html`)
  - `static/network/`: ES-module JS + CSS

## Run locally

### Prerequisites
- Python 3+ (with `pip`)

### Dependencies
Installed via `requirements.txt`:
- Django
- Pillow (required for `ImageField` uploads)

### Setup
```bash
git clone https://github.com/Tyler43222/Qube_Social_Network
cd Qube_Social_Network

python3 -m venv .venv
source .venv/bin/activate

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

### Database + migrations
This repo includes a `db.sqlite3` for demo purposes. If you want a clean database, delete it first.

```bash
python3 manage.py migrate
```

Optional: create an admin user

```bash
python3 manage.py createsuperuser
```

### Start the dev server

```bash
python3 manage.py runserver
```

Then open http://127.0.0.1:8000/

### Database
Currently using SQLite for easy development/demo.

To switch to PostgreSQL for deployment, update `project/settings.py`:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        # configuration details ...
    }
}
```