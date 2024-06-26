from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comments, Genre, Review, Title


class CategorySerializers(serializers.ModelSerializer):
    """Сериализатор для категорий"""

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializers(serializers.ModelSerializer):
    """Сериализатор для жанров"""

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleDetailSerializers(serializers.ModelSerializer):
    """Сериализатор для произведений"""
    genre = GenreSerializers(many=True, read_only=True)
    category = CategorySerializers()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializers(TitleDetailSerializers):
    """Сериализатор для POST-запросов администратора"""
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        required=False
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов"""

    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author',)

    def validate(self, data):
        """Валидация для проверки возможности отзыва не более одного раза"""
        if self.context.get('request').method == 'POST':
            author = self.context['request'].user
            title = self.context['view'].kwargs.get('title_id')
            review = author.review.filter(title=title)
            if review:
                raise serializers.ValidationError(
                    'Пользователь может оставить'
                    'только один отзыв на произведение.'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев"""
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('author',)
