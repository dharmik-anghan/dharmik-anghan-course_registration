from django.urls import path
from review.views import GetReviewView, ReviewView


urlpatterns = [
    path("<int:course_id>/", ReviewView.as_view(), name="review"),
    path("get/<int:course_id>/", GetReviewView.as_view(), name="get-review"),
]
