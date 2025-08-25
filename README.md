# 🎬 Movie Collector

A Django web application for browsing, reviewing, and managing a collection of movies.  
Users can **view movies and reviews publicly**, while logged-in users can **add, edit, and delete** their own movies and reviews.

Created by **Kylie** and **Roger**



## Features

- Public access to all movies and reviews (no login required to view).
- User authentication:
  - **Signup page** for new users.
  - **Login page** for existing users.
  - **Logout** functionality.
- Authenticated users can:
  - Add, update, and delete movies.
  - Add reviews for movies.
  - Delete their reviews.
- Navigation bar with dynamic links based on authentication.
- Clean Django template system with reusable `base.html`.



## Tech Stack

- **Backend:** Django, Python
- **Database:** SQLite (default),switched to PostgreSQL
- **Frontend:** Django templates (HTML, CSS, optional  for movie covers)
- **Auth:** Django’s built-in session-based authentication (Signup/Login/Logout)


