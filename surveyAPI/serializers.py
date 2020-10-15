from rest_framework import serializers
from .models import Survey, Question, QuestionAnswer, UserAnswersHolder, UserAnswer


class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = ['id', 'text']

    def update(self, instance, validated_data):
        instance.text = validated_data.get("text", instance.text)

        instance.save()
        return instance


class QuestionAnswerSerializerWithSpecifiedQuestion(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = ['question', 'text']


class QuestionSerializer(serializers.ModelSerializer):
    question_answers = QuestionAnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'question_answers']

    def update(self, instance, validated_data):
        instance.text = validated_data.get("text", instance.text)
        instance.question_type = validated_data.get("question_type", instance.question_type)

        question_answers_data = validated_data.get("question_answers", None)
        if question_answers_data is not None and instance.question_type != "PT":
            for question_answer in QuestionAnswer.objects.all().filter(question=instance):
                question_answer.delete()

            for question_answer_data in question_answers_data:
                QuestionAnswer.objects.create(question=instance, **question_answer_data)

        if instance.question_type == "PT":
            for question_answer in QuestionAnswer.objects.all().filter(question=instance):
                question_answer.delete()

        instance.save()
        return instance


class QuestionSerializerWithSpecifiedSurvey(serializers.ModelSerializer):
    question_answers = QuestionAnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['survey', 'text', 'question_type', 'question_answers']

    def create(self, validated_data):
        question_answers_data = validated_data.pop("question_answers")
        question = Question.objects.create(**validated_data)
        if question.question_type != "PT":
            for question_answer_data in question_answers_data:
                QuestionAnswer.objects.create(question=question, **question_answer_data)
        return question


class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Survey
        fields = ['id', 'title', 'start_date', 'end_date', 'description', 'questions']

    def create(self, validated_data):
        questions_data = validated_data.pop("questions")
        survey = Survey.objects.create(**validated_data)
        for question_data in questions_data:
            question_answers_data = question_data.pop("question_answers")
            question = Question.objects.create(survey=survey, **question_data)
            if question_data["question_type"] != "PT":
                for question_answer_data in question_answers_data:
                    QuestionAnswer.objects.create(question=question, **question_answer_data)
        return survey

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.end_date = validated_data.get("end_date", instance.end_date)
        instance.description = validated_data.get("description", instance.description)

        questions_data = validated_data.get("questions", None)
        if questions_data is not None:
            current_questions = Question.objects.all().filter(survey=instance)
            for question in current_questions:
                question.delete()

            for question_data in questions_data:
                question_answers_data = question_data.pop("question_answers")
                question = Question.objects.create(survey=instance, **question_data)
                if question_data["question_type"] != "PT":
                    for question_answer_data in question_answers_data:
                        QuestionAnswer.objects.create(question=question, **question_answer_data)
        instance.save()
        return instance


class UserAnswerCreationSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), many=False, read_only=False)

    class Meta:
        model = UserAnswer
        fields = ['question', 'answer']


class UserAnswersHolderCreationSerializer(serializers.ModelSerializer):
    answers = UserAnswerCreationSerializer(many=True, read_only=False)

    class Meta:
        model = UserAnswersHolder
        fields = ['user_ID', 'survey', 'answers']

    @staticmethod
    def check_answers(questions, given_answers):
        all_questions_completed = True
        for question in questions:
            question_completed = False
            for given_answer in given_answers:
                if given_answer["question"] == question:
                    question_completed = True
                    break
            if not question_completed:
                all_questions_completed = False
                break

        if not all_questions_completed:
            raise AttributeError("All questions should be completed!")

        all_choice_questions_correct = True
        for given_answer in given_answers:
            if given_answer["question"].question_type != "PT":
                available_answers = QuestionAnswer.objects.all().filter(question=given_answer["question"])
                choice_question_correct = False
                for available_answer in available_answers:
                    if available_answer.text == given_answer["answer"]:
                        choice_question_correct = True
                if not choice_question_correct:
                    all_choice_questions_correct = False
                    break

        if not all_choice_questions_correct:
            raise ValueError("Choice questions should be chosen correctly!")

    def create(self, validated_data):
        survey = Survey.objects.all().get(pk=validated_data.get("survey").id)
        questions = Question.objects.all().filter(survey=survey)
        given_answers = validated_data.pop("answers")

        self.check_answers(questions, given_answers)

        user_answers_holder = UserAnswersHolder.objects.create(**validated_data)

        for question in questions:
            multiply_choices_answers = []
            for given_answer in given_answers:
                if given_answer["question"] == question:
                    if question.question_type == "MC" and given_answer["answer"] in multiply_choices_answers:
                        continue
                    UserAnswer.objects.create(user_answers_holder=user_answers_holder, **given_answer)
                    multiply_choices_answers.append(given_answer["answer"])
                    if question.question_type != "MC":
                        break
        return user_answers_holder


class UserAnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = UserAnswer
        fields = ['question', 'answer']


class UserAnswersHolderSerializer(serializers.ModelSerializer):
    answers = UserAnswerSerializer(many=True, read_only=True)
    survey = SurveySerializer(many=False, read_only=True)

    class Meta:
        model = UserAnswersHolder
        fields = ['id', 'user_ID', 'survey', 'answers']
