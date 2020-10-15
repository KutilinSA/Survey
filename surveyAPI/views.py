from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.status import HTTP_400_BAD_REQUEST

from .models import Survey, UserAnswersHolder
from .serializers import SurveySerializer, UserAnswersHolderCreationSerializer, UserAnswersHolderSerializer

from datetime import datetime


class SurveyView(ViewSet):
    """
    Класс, описывающий методы взаимодействия пользователя с опросами
    """
    @staticmethod
    def list(request):
        """
        Сериализует список всех объектов типа Survey
        :param request: запрос
        :return: ответ на запрос, содержащий сериализованный список объектов
        """
        surveys = Survey.objects.all().filter(end_date__gte=datetime.now().date())
        serializer = SurveySerializer(surveys, many=True)
        return Response({"surveys": serializer.data})

    @staticmethod
    def retrieve(request, pk):
        """
        Сериализует объект типа Survey с id равным pk.
        :param request: запрос
        :param pk: id необходимого объекта
        :return: ответ на запрос, содержащий сериализованный объект
        """
        surveys = Survey.objects.all().filter(end_date__gte=datetime.now().date())
        survey = get_object_or_404(surveys, pk=pk)
        serializer = SurveySerializer(instance=survey)
        return Response({"survey": serializer.data})

    @staticmethod
    def complete_survey(request, pk):
        """
        Метод прохождения опроса
        :param request: запрос
        :param pk: id необходимого опроса
        :return: ответ на запрос, содержащий информацию о ходе выполнения действия
        """
        surveys = Survey.objects.all().filter(end_date__gte=datetime.now().date())
        survey = get_object_or_404(surveys, pk=pk)
        data = request.data.get("user_answers", {})
        data["survey"] = survey.id
        serializer = UserAnswersHolderCreationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save()
            except AttributeError as e:
                return Response({(str(e))}, status=HTTP_400_BAD_REQUEST)
            except ValueError as e:
                return Response({(str(e))}, status=HTTP_400_BAD_REQUEST)
            return Response({"Your answer was saved"}, status=201)
        return Response({"Incorrect data!"}, status=HTTP_400_BAD_REQUEST)


class CompletedSurveyView(ViewSet):
    @staticmethod
    def list(request, user_id):
        completed_surveys = UserAnswersHolder.objects.all().filter(user_ID=user_id)
        serializer = UserAnswersHolderSerializer(completed_surveys, many=True)
        return Response({"completed_surveys": serializer.data})

    @staticmethod
    def retrieve(request, user_id, pk):
        completed_surveys = UserAnswersHolder.objects.all().filter(user_ID=user_id)
        completed_survey = get_object_or_404(completed_surveys, pk=pk)
        serializer = UserAnswersHolderSerializer(instance=completed_survey)
        return Response({"completed_survey": serializer.data})
