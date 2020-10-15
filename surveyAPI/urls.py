from django.urls import path

from .views import SurveyView, CompletedSurveyView

urlpatterns = [
    path("surveys/", SurveyView.as_view({"get": "list"})),
    path("surveys/<int:pk>", SurveyView.as_view({"get": "retrieve", "post": "complete_survey"})),
    path("completed-surveys/<int:user_id>",  CompletedSurveyView.as_view({"get": "list"})),
    path("completed-surveys/<int:user_id>/<int:pk>",  CompletedSurveyView.as_view({"get": "retrieve"})),
]
