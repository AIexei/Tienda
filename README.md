# TIENDA
Online shop

## Installation
Make virtualenv (with Python3+):
 * `virtualenv python=python3 'env_name'`
 * `activate virtualenv`
 * `pip install django==1.11.2`
 * `pip install Pillow==4.1.1`
 * `pip install django-mptt==0.8.7`
 * `pip install django-ratelimit==1.0.1`
 * `pip install psycopg2==2.7.1 (for PostgreSQL db)`
 
Clone project:
 * `git clone https://alexei.evlanov@gitlab.itechart-group.com/d2.st.shop/shop.git`
 * `configure your database (watch .../shop/shop/settings.py DATABASES)`
 * `python manage.py makemigrations`
 * `python manage.py migrate`

## Usage
 * `activate your environment`
 * `python manage.py runserver`
 * `enjoy it :D`
