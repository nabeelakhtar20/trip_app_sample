# Trip App Sample Api
This is a repository for a trip planning mobile apa api's developed with with Django and Neo4j as Graph database and Google Place API.

### Features
1. **Local Authentication** using email and password.
2. **Rest API** using [django rest framework](http://www.django-rest-framework.org/)
4. **Neo4j** as Graph Database
5. **Google Place API** for searching places in destination city

### API's
1. **Register User API**
2. **Login User API**
3. **Get User Details API**
4. **Add favourites in user profile API**
5. **Create Trip API**
6. **Get Trip Details API**
7. **Update Trip API**
8. **Explore City API (with user_id as parameter)**
9. **Explore City API (with pageToken as parameter)**
10. **Explore City API (with city_name and interest as parameters)**
11. **Explore City API (with city_name and user_id as parameter)**

### Recommended Installation
1. [Neo4j](https://neo4j.com/download/)
2. [Python3.6](https://www.python.org/downloads/release/python-365/)

### Installation
1. Install python
2. Install pip
3. Clone this repo and `cd trip_app_sample`
4. Run `pip install -r requirement.txt`
5. Update settings file `DATABASE_URL` with neo4j credentials.
6. Update settings file `GOOGLE_MAP_PLACE_API_KEY`.

### Getting Started
1. Run `python manage.py runserver`

### API Documentation
https://documenter.getpostman.com/view/729372/SVtPXAVi?version=latest

Use this documentation to find about request, response and end url's