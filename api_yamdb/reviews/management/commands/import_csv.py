from pathlib import Path
from os.path import join
import csv
import io

from django.core.management.base import BaseCommand

from reviews import models

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

CATEGORY = {
    'id': 0,
    'name': 1,
    'slug': 2,
}

COMMENT = {
    'id': 0,
    'review_id': 1,
    'text': 2,
    'author': 3,
    'pub_date': 4,
}

GENRE = {
    'id': 0,
    'name': 1,
    'slug': 2,
}

TITLE = {
    'id': 0,
    'name': 1,
    'year': 2,
    'category': 3,
}

REVIEW = {
    'id': 0,
    'title_id': 1,
    'text': 2,
    'author': 3,
    'score': 4,
    'pub_date': 5,
}

GENRE_TITLE = {
    'id': 0,
    'title_id': 1,
    'genre_id': 2,
}

USERS = {
    'id': 0,
    'username': 1,
    'email': 2,
    'role': 3,
    'bio': 4,
    'first_name': 5,
    'last_name': 6,
}


class Command(BaseCommand):
    help = 'Import csv files with data to SQL database'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        STATIC_FOLDER = join(BASE_DIR, 'static')
        DATA_FOLDER = join(STATIC_FOLDER, 'data')

        csvfile = io.open(join(DATA_FOLDER, 'users.csv'), encoding="utf-8")
        next(csvfile)
        file = csv.reader(csvfile, delimiter=',')
        for row in file:
            models.User.objects.create(
                id=row[USERS['id']],
                username=row[USERS['username']],
                email=row[USERS['email']],
                role=row[USERS['role']],
                bio=row[USERS['bio']],
                first_name=row[USERS['first_name']],
                last_name=row[USERS['last_name']],
            )

        csvfile = io.open(join(DATA_FOLDER, 'category.csv'), encoding="utf-8")
        next(csvfile)
        file = csv.reader(csvfile, delimiter=',')
        for row in file:
            models.Category.objects.create(
                id=row[CATEGORY['id']],
                name=row[CATEGORY['name']],
                slug=row[CATEGORY['slug']],
            )

        csvfile = io.open(join(DATA_FOLDER, 'genre.csv'), encoding="utf-8")
        next(csvfile)
        file = csv.reader(csvfile, delimiter=',')
        for row in file:
            models.Genre.objects.create(
                id=row[GENRE['id']],
                name=row[GENRE['name']],
                slug=row[GENRE['slug']],
            )

        csvfile = io.open(join(DATA_FOLDER, 'genre_title.csv'),
                          encoding="utf-8")
        next(csvfile)
        file = csv.reader(csvfile, delimiter=',')
        genre_titles = {}
        for row in file:
            if row[GENRE_TITLE['title_id']] in genre_titles:
                genre_titles[row[GENRE_TITLE['title_id']]].append(
                    models.Genre.objects.get(id=row[GENRE_TITLE['genre_id']])
                )
            else:
                genre_titles[row[GENRE_TITLE['title_id']]] = [
                    models.Genre.objects.get(id=row[GENRE_TITLE['genre_id']]),
                ]

        csvfile = io.open(join(DATA_FOLDER, 'titles.csv'), encoding="utf-8")
        next(csvfile)
        file = csv.reader(csvfile, delimiter=',')
        for row in file:
            category = models.Category.objects.get(id=row[TITLE['category']])
            genres = genre_titles[row[TITLE['id']]]
            title = models.Title.objects.create(
                id=row[TITLE['id']],
                name=row[TITLE['name']],
                year=row[TITLE['year']],
                category=category,
            )
            title.genre.set(genres)

        csvfile = io.open(join(DATA_FOLDER, 'review.csv'), encoding="utf-8")
        next(csvfile)
        file = csv.reader(csvfile, delimiter=',')
        for row in file:
            author = models.User.objects.get(id=row[REVIEW['author']])
            title = models.Title.objects.get(id=row[REVIEW['title_id']])
            models.Review.objects.create(
                id=row[REVIEW['id']],
                text=row[REVIEW['text']],
                author=author,
                title=title,
                score=row[REVIEW['score']],
                pub_date=row[REVIEW['pub_date']],
            )

        csvfile = io.open(join(DATA_FOLDER, 'comments.csv'), encoding="utf-8")
        next(csvfile)
        file = csv.reader(csvfile, delimiter=',')
        for row in file:
            author = models.User.objects.get(id=row[COMMENT['author']])
            review = models.Review.objects.get(id=row[COMMENT['review_id']])
            models.Comment.objects.create(
                id=row[COMMENT['id']],
                text=row[COMMENT['text']],
                author=author,
                review=review,
                pub_date=row[COMMENT['pub_date']],
            )
