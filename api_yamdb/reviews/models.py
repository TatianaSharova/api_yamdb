import datetime as dt

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Наименование категории'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Название'
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Наименование Жанра'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Название'
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Наименование'
    )
    year = models.IntegerField(db_index=True)
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genre',
        through='GenreTitle'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='category',
        blank=True,
        null=True,
        verbose_name='категория'
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name

    def validate(year):
        if dt.datetime.now().year <= year:
            raise ValidationError(
                'Этот год еще не наступил!'
            )


class GenreTitle(models.Model):
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        ...


class Reviews(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review'
    )
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='review'
    )
    text = models.TextField()
    score = models.PositiveIntegerField(validators=[MinValueValidator(1),
                                                    MaxValueValidator(10)])
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text


class Comments(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment'
    )
    review = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        related_name='comment'
    )
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.text