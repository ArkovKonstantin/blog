from django.contrib import auth
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError, AuthenticationFailed, NotAuthenticated
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import ModelSerializer, CharField

from .models import Topic, Comment, TopicLike

"""----------Topic----------"""


class TopicSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='api:topic-detail',
        lookup_field='pk'
    )

    class Meta:
        model = Topic
        fields = '__all__'
        read_only_fields = ['number_of_comments', 'number_of_likes', 'creator', 'created']

    def validate(self, data):
        # import ipdb;
        # ipdb.set_trace()  # BREAKPOINT
        data['creator'] = self.context['request'].user
        return data


class TopicListSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class TopicDetailSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


"""----------User----------"""


class UserUrlSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='api:user-detail',
        lookup_field='pk'
    )

    class Meta:
        model = User
        fields = ['url']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserLoginSerializer(ModelSerializer):
    username = CharField()

    # url = HyperlinkedIdentityField(
    #     view_name='api:detail',
    #     lookup_field='pk'
    # )

    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]
        # read_only_fields = ['first_name', 'last_name', 'email', 'date_joined']
        extra_kwargs = {'passwords': {'write_only': True}}

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        # if not username or not password:
        #     raise ValidationError('Invalid input')

        user = auth.authenticate(username=username, password=password)

        if user:
            data['user'] = user
            return data

        else:
            raise AuthenticationFailed('Invalid username && password')


"""----------Comment----------"""


class CommentCreateSerializer(ModelSerializer):
    # url = HyperlinkedIdentityField(
    #     view_name='api:comment-detail',
    #     lookup_field='pk'
    # )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['creator', 'created']

    def validate(self, data):
        data['creator'] = self.context['request'].user
        return data


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


"""----------Like----------"""


class LikeSerializer(ModelSerializer):
    class Meta:
        model = TopicLike
        fields = '__all__'


class LikeCreateSerializer(ModelSerializer):
    class Meta:
        model = TopicLike
        fields = ['topic']

    def validate(self, data):
        data['user'] = self.context['request'].user
        return data
