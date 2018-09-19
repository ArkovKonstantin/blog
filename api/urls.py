from django.conf.urls import url
from django.urls import path

from api.views import CreateTopic, TopicList, UserLoginAPIView, LogoutView, UserDetailAPIView, TopicDetailAPIView, \
    CreateComment, CommentDetailAPIView, CommentList, TopicLike, LikeDetailAPIView, CreateLike

app_name = 'api'

urlpatterns = [
    url(r'^user/(?P<pk>\d+)/$', UserDetailAPIView.as_view(), name='user-detail'),
    url(r'^topic/(?P<pk>\d+)/$', TopicDetailAPIView.as_view(), name='topic-detail'),
    url(r'^comment/(?P<pk>\d+)/$', CommentDetailAPIView.as_view(), name='comment-detail'),
    url(r'^like/(?P<pk>\d+)/$', LikeDetailAPIView.as_view(), name='like-detail'),
]

topic_patterns = [
    path('create/', CreateTopic.as_view()),
    path('list/', TopicList.as_view()),
    path('like/', CreateLike.as_view()),

]

auth_patterns = [
    path('login/', UserLoginAPIView.as_view()),
    path('logout/', LogoutView.as_view()),
]

comment_patterns = [
    path('create/', CreateComment.as_view()),
    path('list/', CommentList.as_view()),
]
