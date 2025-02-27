from django.urls import path , include
from .views import *


urlpatterns = [

    path('blog/', blog, name='blog'),
    path('blog/<int:id>/',blog, name='blog'),
    path('blog_detail/', blog_detail, name='blog_detail'),
    path('blog_detail/<int:id>',blog_detail, name='blog_detail'),
    path('blog_review/<int:id>/', submit_review_blog, name='blog_review'),

]