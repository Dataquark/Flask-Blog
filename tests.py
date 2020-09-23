from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post


class UserModelCase(unittest.TestCase):
    # create an in-memory SQLite db
    # create_all() creates all the dbs at once
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        db.create_all()

    # removes the db from the memory
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username="Mark")
        u.set_password("Kefir")
        self.assertFalse(u.check_password("Milk"))
        self.assertTrue(u.check_password("Kefir"))

    def test_avatar(self):
        u = User(username="john", email="john@example.com")
        self.assertEqual(
            u.avatar(128),
            "https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?d=identicon&s=128",
        )

    def test_follow(self):
        u1 = User(username="Kate", email="kate@example.com")
        u2 = User(username="Brad", email="brad@example.com")
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, "Brad")
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, "Kate")

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # create 4 users
        u1 = User(username="Alice", email="alice@example.com")
        u2 = User(username="Bobby", email="bobby@example.com")
        u3 = User(username="Corey", email="corey@example.com")
        u4 = User(username="Daisy", email="daisy@example.com")
        db.session.add_all([u1, u2, u3, u4])

        # create 4 posts
        now = datetime.now()
        p1 = Post(
            body="Post from Alice", author=u1, timestamp=now + timedelta(seconds=1)
        )
        p2 = Post(
            body="Post from Bobby", author=u2, timestamp=now + timedelta(seconds=4)
        )
        p3 = Post(
            body="Post from Corey", author=u3, timestamp=now + timedelta(seconds=3)
        )
        p4 = Post(
            body="Post from Daisy", author=u4, timestamp=now + timedelta(seconds=2)
        )
        db.session.commit()

        # setup the followers
        u1.follow(u2)
        u1.follow(u4)
        u2.follow(u3)
        u3.follow(u4)
        db.session.commit()

        # check the followed post for each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])


if __name__ == "__main__":
    unittest.main(verbosity=2)
