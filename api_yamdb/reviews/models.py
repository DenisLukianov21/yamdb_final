from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import UsernameRegexValidator


class User(AbstractUser):
    """Модель Юзера."""
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER_ROLE = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )
    username = models.CharField('Никнейм пользователя',
                                validators=(UsernameRegexValidator,),
                                max_length=225, unique=True)
    email = models.EmailField('Почта пользователя', unique=True)
    bio = models.TextField('О себе', blank=True)
    role = models.CharField(
        'Роль пользователя', max_length=50,
        choices=USER_ROLE, default=USER
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class CommentReviewAbstract(models.Model):
    """Абстрактная модель для Отзывов и коментов."""
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True)
    text = models.TextField(null=False)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
        db_index=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.author


class GenreCategory(models.Model):
    """Абстрактная модель для категорий и жанров."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        db_index=True
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(GenreCategory):
    """Модель Категорий."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Genre(GenreCategory):
    """Модель Жанров."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)


class Title(models.Model):
    """Модель Произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения',
        db_index=True
    )
    year = models.IntegerField(
        verbose_name='Год создания произведения',
        db_index=True,
        validators=(
            MaxValueValidator(
                int(datetime.now().year),
                message='Произведение не может быть из будущего!!111!'
            ),
        )
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание произведения'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='Жанр',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year', 'name')

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель связывающая жанры и произведения."""
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    class Meta:
        verbose_name = 'Произведение относится к жанру'
        verbose_name_plural = 'Произведение относится к жанрам'
        ordering = ('id',)

    def __str__(self):
        return f'{self.title} принадлежит жанру(жанрам) {self.genre}'


class Review(CommentReviewAbstract):
    """Модель отзыва."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        db_index=True
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=(
            MinValueValidator(1, 'Минимальная оценка 1',),
            MaxValueValidator(10, 'Максимальная 10',)
        ),
    )

    class Meta:
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_title_author'
            ),
        )

    def __str__(self):
        return self.text[:15]


class Comment(CommentReviewAbstract):
    """Модель комментария."""
    review = models.ForeignKey(
        Review,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]
