from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST

from surveyAPI.models import Survey, Question, QuestionAnswer
from surveyAPI.serializers import SurveySerializer, QuestionSerializer, QuestionAnswerSerializer,\
    QuestionAnswerSerializerWithSpecifiedQuestion, QuestionSerializerWithSpecifiedSurvey

from abc import ABC, abstractmethod


class FullManagementView(ABC):
    """Абстрактный класс FullManagementView

    Описывает все необходимые методы, для осуществления полного контроля над базой данных.
    Для использования необходимо создать класс-наследник, переопределяющий target, target_serializer и target_string

    Necessary properties:
        target: target model for control
        target_serializer: serializer for target model
        target_string: string that represents target model
    """

    @property
    @abstractmethod
    def target(self):
        pass

    @property
    @abstractmethod
    def target_serializer(self):
        pass

    @property
    @abstractmethod
    def target_string(self):
        pass

    def list(self, request, objects=None):
        """
        Сериализует список всех объектов типа target при objects=None,
        иначе сериализует список всех объектов из objects.
        :param request: запрос
        :param objects: список объектов. None, если требуется получить все объекты типа target
        :return: ответ на запрос, содержащий сериализованный список объектов
        """
        if not request.user.is_authenticated:
            return Response({"You are not authorized!"}, status=HTTP_401_UNAUTHORIZED)
        if not request.user.is_superuser and not request.user.is_staff:
            return Response({"You are not allowed to add new surveys!"}, status=HTTP_403_FORBIDDEN)
        if objects is None:
            objects = self.target.objects.all()
        serializer = self.target_serializer(objects, many=True)
        return Response({self.target_string.lower() + "s": serializer.data})

    def retrieve(self, request, pk, objects=None):
        """
        Сериализует объект типа target с id равным pk.
        :raises: HTTP 404 error, если не найден объект
        :param request: запрос
        :param pk: id необходимого объекта
        :param objects: список, в котором происходит поиск. Если None, поиск идет по всем объектам
        :return: ответ на запрос, содержащий сериализованный объект
        """
        if not request.user.is_authenticated:
            return Response({"You are not authorized!"}, status=HTTP_401_UNAUTHORIZED)
        if not request.user.is_superuser and not request.user.is_staff:
            return Response({"You are not allowed to add new surveys!"}, status=HTTP_403_FORBIDDEN)
        if objects is None:
            objects = self.target.objects.all()
        obj = get_object_or_404(objects, pk=pk)
        serializer = self.target_serializer(instance=obj)
        return Response({self.target_string.lower(): serializer.data})

    def create(self, request, serializer=None):
        """
        Метод для создания объекта и записи его в базу данных
        :param request: запрос
        :param serializer: необходимый сериализатор. Если None, то используется target_serializer
        :return: ответ на запрос, содержащий информацию о ходе выполнения действия
        """
        if not request.user.is_authenticated:
            return Response({"You are not authorized!"}, status=HTTP_401_UNAUTHORIZED)
        if not request.user.is_superuser and not request.user.is_staff:
            return Response({"You are not allowed to add new surveys!"}, status=HTTP_403_FORBIDDEN)
        if serializer is None:
            serializer = self.target_serializer
        data = request.data.get(self.target_string.lower(), None)
        serializer = serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            obj = serializer.save()
            return Response({self.target_string.capitalize() + " ({}) was created".format(obj.id)}, status=201)
        return Response({"Incorrect data!"}, status=HTTP_400_BAD_REQUEST)

    def update(self, request, pk, objects=None):
        """
        Обновляет поля объекта с id равным pk присланной информацией
        :param request: запрос
        :param pk: id объекта
        :param objects: список, в котором происходит поиск объекта. Если None, поиск идет по всем объектам
        :return: ответ на запрос, содержащий информацию о ходе выполнения действия
        """
        if not request.user.is_authenticated:
            return Response({"You are not authorized!"}, status=HTTP_401_UNAUTHORIZED)
        if not request.user.is_superuser and not request.user.is_staff:
            return Response({"You are not allowed to add new surveys!"}, status=HTTP_403_FORBIDDEN)
        if objects is None:
            objects = self.target.objects.all()
        obj = get_object_or_404(objects, pk=pk)
        data = request.data.get(self.target_string.lower(), None)
        serializer = self.target_serializer(instance=obj, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            obj = serializer.save()
            return Response({self.target_string.capitalize() + " ({}) was updated".format(obj.id)})
        return Response({"Incorrect data!"}, status=HTTP_400_BAD_REQUEST)

    def remove(self, request, pk, objects=None):
        """
        Удаляет объект с id равным pk
        :param request: запрос
        :param pk: id объекта
        :param objects: список, в котором происходит поиск объекта. Если None, поиск идет по всем объектам
        :return: ответ на запрос, содержащий информацию о ходе выполнения действия
        """
        if not request.user.is_authenticated:
            return Response({"You are not authorized!"}, status=HTTP_401_UNAUTHORIZED)
        if not request.user.is_superuser and not request.user.is_staff:
            return Response({"You are not allowed to add new surveys!"}, status=HTTP_403_FORBIDDEN)
        if objects is None:
            objects = self.target.objects.all()
        obj = get_object_or_404(objects, pk=pk)
        obj.delete()
        return Response({self.target_string.capitalize() + " ({}) was deleted".format(pk)})


class SurveyView(viewsets.ViewSet, FullManagementView):
    """

    """

    @property
    def target(self):
        return Survey

    @property
    def target_serializer(self):
        return SurveySerializer

    @property
    def target_string(self):
        return "survey"

    def retrieve(self, request, survey_pk, objects=None):
        return super().retrieve(request, survey_pk)

    def create(self, request, serializer=None):
        return super().create(request)

    def update(self, request, survey_pk, objects=None):
        return super().update(request, survey_pk)

    def remove(self, request, survey_pk, objects=None):
        return super().remove(request, survey_pk)


class QuestionView(viewsets.ViewSet, FullManagementView):
    @property
    def target(self):
        return Question

    @property
    def target_serializer(self):
        return QuestionSerializer

    @property
    def target_string(self):
        return "question"

    @staticmethod
    def get_objects(survey_pk):
        if survey_pk is None:
            return None
        survey = get_object_or_404(Survey.objects.all(), pk=survey_pk)
        return Question.objects.all().filter(survey=survey)

    def list(self, request, survey_pk=None):
        return super().list(request, self.get_objects(survey_pk))

    def retrieve(self, request, survey_pk=None, question_pk=None):
        return super().retrieve(request, question_pk, self.get_objects(survey_pk))

    def create(self, request, survey_pk=None):
        if survey_pk is not None:
            survey = get_object_or_404(Survey.objects.all(), pk=survey_pk)
            request.data.get("question", {})["survey"] = survey.id
        return super().create(request, QuestionSerializerWithSpecifiedSurvey)

    def update(self, request, survey_pk=None, question_pk=None):
        return super().update(request, question_pk, self.get_objects(survey_pk))

    def remove(self, request, survey_pk=None, question_pk=None):
        return super().remove(request, question_pk, self.get_objects(survey_pk))


class QuestionAnswerView(viewsets.ViewSet, FullManagementView):
    @property
    def target(self):
        return QuestionAnswer

    @property
    def target_serializer(self):
        return QuestionAnswerSerializer

    @property
    def target_string(self):
        return "question_answer"

    @staticmethod
    def get_objects(survey_pk=None, question_pk=None):
        if survey_pk is None and question_pk is None:
            return None
        if survey_pk is not None:
            survey = get_object_or_404(Survey.objects.all(), pk=survey_pk)
            if question_pk is None:
                objects = QuestionAnswer.objects.all().filter(question__survey=survey)
            else:
                questions = Question.objects.all().filter(survey=survey)
                question = get_object_or_404(questions, pk=question_pk)
                objects = QuestionAnswer.objects.all().filter(question=question)
            return objects
        else:
            question = get_object_or_404(Question.objects.all(), pk=question_pk)
            objects = QuestionAnswer.objects.all().filter(question=question)
            return objects

    def list(self, request, survey_pk=None, question_pk=None):
        return super().list(request, self.get_objects(survey_pk, question_pk))

    def retrieve(self, request, survey_pk=None, question_pk=None, question_answer_pk=None):
        return super().retrieve(request, question_answer_pk, self.get_objects(survey_pk, question_pk))

    def create(self, request, survey_pk=None, question_pk=None):
        if question_pk is not None:
            if survey_pk is not None:
                survey = get_object_or_404(Survey.objects.all(), pk=survey_pk)
                questions = Question.objects.all().filter(survey=survey)
                question = get_object_or_404(questions, pk=question_pk)
            else:
                question = get_object_or_404(Question.objects.all(), pk=question_pk)
            request.data.get("question_answer", {})["question"] = question.id
        return super().create(request, QuestionAnswerSerializerWithSpecifiedQuestion)

    def update(self, request, survey_pk=None, question_pk=None, question_answer_pk=None):
        return super().update(request, question_answer_pk, self.get_objects(survey_pk, question_pk))

    def remove(self, request, survey_pk=None, question_pk=None, question_answer_pk=None):
        return super().remove(request, question_answer_pk, self.get_objects(survey_pk, question_pk))
