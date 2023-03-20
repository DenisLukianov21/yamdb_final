from django.utils import timezone
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import UsernameRegexValidator


class CategorySerializer(serializers.ModelSerializer):
    """Сериалезатор для Category."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериалезатор для Genre."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleCUDSerializer(serializers.ModelSerializer):
    """Сериалезатор для Title при CREATE, UPDATE, DELETE запросах."""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )

    def validate_year(self, value):
        year = timezone.datetime.now().year
        if value > year:
            raise serializers.ValidationError(
                f'Год выпуска не может быть больше {year}'
            )
        return value


class TitleGETSerializer(serializers.ModelSerializer):
    """Сериалезатор для Title при GET запросах."""
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta():
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )


class UserSerializer(serializers.ModelSerializer):
    """ Сериализация юзера. """

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        )
        read_only_field = ('role',)


class CommentSerializer(serializers.ModelSerializer):
    """ Сериализация комментария. """
    author = SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        model = Comment
        exclude = ('review',)


class ReviewSerializer(serializers.ModelSerializer):
    """ Сериализация отзыва. """
    author = SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )

    class Meta:
        model = Review
        fields = (
            'id', 'text', 'author', 'score', 'pub_date', 'title')

    def validate(self, data):
        if self.context['request'].method == 'POST':
            author = self.context['request'].user
            title = self.context['view'].kwargs.get('title_id')
            if Review.objects.filter(author=author, title__id=title).exists():
                raise serializers.ValidationError('Отзыв уже есть.')
        return data


class SingUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации."""

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" не разрешено.'
            )
        return value


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена при регистрации."""

    username = serializers.CharField(
        required=True,
        validators=(UsernameRegexValidator(), )
    )
    confirmation_code = serializers.CharField(required=True)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" не разрешено.'
            )
        return value
