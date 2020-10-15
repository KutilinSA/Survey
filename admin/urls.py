from django.urls import path, include

from .admin_full_management import SurveyView, QuestionView, QuestionAnswerView
from rest_framework.authtoken.views import obtain_auth_token

GENERAL_METHODS = {"get": "list", "post": "create"}
SPECIFIED_METHODS = {"get": "retrieve", "put": "update", "delete": "remove"}

questions_answers_urlpatterns = [
    path("questions-answers/", QuestionAnswerView.as_view(GENERAL_METHODS)),
    path("questions-answers/<int:question_answer_pk>", QuestionAnswerView.as_view(SPECIFIED_METHODS)),
]

questions_urlpatterns = [
    path("questions/", QuestionView.as_view(GENERAL_METHODS)),
    path("questions/<int:question_pk>", QuestionView.as_view(SPECIFIED_METHODS)),
    path("questions/<int:question_pk>/", include(questions_answers_urlpatterns))
]

urlpatterns = [
    path("surveys/", SurveyView.as_view(GENERAL_METHODS)),
    path("surveys/<int:survey_pk>", SurveyView.as_view(SPECIFIED_METHODS)),
    path("surveys/<int:survey_pk>/", include(questions_urlpatterns)),
    path("surveys/<int:survey_pk>/", include(questions_answers_urlpatterns)),

    path("", include(questions_urlpatterns)),
    path("", include(questions_answers_urlpatterns)),
    path("login/", obtain_auth_token)
]