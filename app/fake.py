from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User, Post

fake = Faker()

def users(count=100):
  i = 0
  while i < count:
    u = User(email=fake.email(), username=fake.user_name(), password='password', confirmed=True, name=fake.name(), location=fake.city(), about_me=fake.text(), member_since=fake.date_time())
    db.session.add(u)
    try:
      db.session.commit()
      i += 1
    except IntegrityError:
      db.session.rollback()

def posts(count=100):
  user_count = User.query.count()
  for i in range(count):
    u = User.query.offset(randint(0, user_count - 1)).first()
    p = Post(body = fake.text(), timestamp=fake.date_time(), author=u)
    db.session.add(p)
  db.session.commit()