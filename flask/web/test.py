from app import models, db
users = models.User.query.all()
for u in users:
    db.session.delete(u)

posts = models.Post.query.all()
for p in posts:
    db.session.delete(p)

db.session.commit()