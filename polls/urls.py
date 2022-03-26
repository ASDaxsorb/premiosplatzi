from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    #e.g: /polls/
    path("", views.IndexView.as_view(), name="index"),
    #e.g: /polls/5
    path("detail/<int:pk>", views.DetailView.as_view(), name="detail"),
    #e.g: /polls/5/results
    path("results/<int:pk>", views.ResultsView.as_view(), name="results"),
    #e.g: /polls/5/vote
    path("vote/<int:question_id>", views.vote, name="vote"),
]