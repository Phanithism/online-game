from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('online_game.db')

class User(UserMixin, Model):
    username = CharField(unique = True)
    password = CharField(max_length = 1000)
    joint_at = TimestampField(null = True)

    class Meta:
        database = DATABASE

    def get_games(self):
        return Game.select().where(Game.user == self)

    @classmethod
    def new(cls, username, password):
        try:
            cls.create(username = username, password = generate_password_hash(password))
        except IntegrityError:
            raise ValueError("User bad value")

class Game(Model):
    name = CharField(unique = True)
    embed_url = CharField(unique = True)
    description = CharField()
    created_at = TimestampField(null = True)
    logo = CharField()
    user = ForeignKeyField(rel_model = User, related_name = 'games')

    class Meta:
        database = DATABASE
        order_by = ('-created_at',)

    def get_user(self):
        return User.where


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Game], safe = True)
    # User.new(username = 'Phanith', password = '1234567890')
