from django.contrib import auth
from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from datetime import datetime

from .serializers import (TopicSerializer,
                          UserLoginSerializer,
                          UserSerializer,
                          UserUrlSerializer,
                          TopicDetailSerializer, TopicListSerializer, CommentSerializer,
                          CommentCreateSerializer, LikeSerializer, LikeCreateSerializer)
from .models import Topic, Comment, TopicLike

"""---------------DetailAPI---------------"""


class UserDetailAPIView(RetrieveAPIView):
    # permission_classes = [AllowAny]
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TopicDetailAPIView(RetrieveAPIView):
    # permission_classes = [AllowAny]
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    queryset = Topic.objects.all()
    serializer_class = TopicDetailSerializer


class CommentDetailAPIView(RetrieveAPIView):
    # permission_classes = [AllowAny]
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    queryset = Topic.objects.all()
    serializer_class = CommentSerializer


class LikeDetailAPIView(RetrieveAPIView):
    # permission_classes = [AllowAny]
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    queryset = TopicLike.objects.all()
    serializer_class = LikeSerializer


"""---------------CreateAPI---------------"""


class CreateLike(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = LikeCreateSerializer
    queryset = TopicLike.objects.all()
    period = 30  # время, в течение которого можно отменить лайк

    def post(self, request, *args, **kwargs):
        # import ipdb
        # ipdb.set_trace()  # BREAKPOINT
        serializer = LikeCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        topic = serializer.validated_data['topic']
        user = serializer.validated_data['user']
        like = TopicLike.objects.filter(topic=topic, user=user)

        if request.session.get(str(topic.pk), None):
            if (datetime.now() - datetime.strptime(request.session[str(topic.pk)],
                                                   '%Y-%m-%d %H:%M:%S.%f')).seconds <= self.period:
                if like:
                    like.delete()
                    topic.number_of_likes -= 1
                    topic.save()
                    return Response({'topic_id': topic.pk, 'user_id': user.pk}, status=HTTP_200_OK)
                else:
                    TopicLike.objects.create(topic=topic, user=user)
                    topic.number_of_likes += 1
                    topic.save()
                    return Response({'topic_id': topic.pk, 'user_id': user.pk}, status=HTTP_200_OK)
            else:
                return Response(status=403)
        else:
            TopicLike.objects.create(topic=topic, user=user)
            topic.number_of_likes += 1
            topic.save()
            request.session[str(topic.pk)] = str(datetime.now())
            return Response({'topic_id': topic.pk, 'user_id': user.pk}, status=HTTP_200_OK)


class CreateTopic(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class CreateComment(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        try:
            topic = get_object_or_404(Topic, pk=serializer.validated_data['topic'].pk)
            topic.number_of_comments += 1
            topic.save()
        except ObjectDoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=HTTP_200_OK, headers=headers)


"""---------------ListAPI---------------"""


class TopicList(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get(self, request):
        topics = Topic.objects.all()
        serializer = TopicListSerializer(topics, many=True)
        return Response(serializer.data)


class CommentList(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


"""---------LoginAPI & LogoutAPI--------"""


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        # import pdb;
        # pdb.set_trace()  # BREAKPOINT
        data = request.data

        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            auth.login(request, user)  # create sessionid
            token, created = Token.objects.get_or_create(user=user)  # create token

            users = Topic.objects.filter(pk=user.pk)
            # {'token': token.key}
            return Response(
                {'id': user.id, 'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name,
                 'email': user.email,
                 'date_joined': user.date_joined}, status=HTTP_200_OK)

        return Response({'detail': 'Invalid input'}, status=HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request):
        auth.logout(request)  # remove sessionid
        return Response(status=200)
