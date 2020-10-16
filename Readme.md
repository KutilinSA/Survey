# Survey Project
## Deploy
To deploy project do next steps:
- install MySQL and create user with username=\"Survey\" and password=\"Qwerty123_\" (or change it in Settings.py)
- give all privileges to it
- create database named \"Database\" (or change it in Settings.py)
- download the repository using GIT
- create python virtual environment
- install requirements (`pip install -r requirements.txt`)
- apply migrations (`python manage.py migrate`)
- create user for system (`python manage.py createsuperuser`)
- generate token for him (`python manage.py drf_create_token`)
Then connect your server with wsgi module (see your server docs). Else you can run project without real server just for test. Use `python manage.py runserver` command for this, then open any REST (you can even use plugins for browser) and make you requests to http://127.0.0.1:8000

## How to work

Note: all payloads examples see in \"examples\" folder

You can use (not admin):
 - \<your host url\>/api/surveys
 - - GET method: get all actual surveys
 - \<your host url\>/api/surveys/\<survey id\>/
 - - GET method: retrieve survey with the given id
 - - POST method: complete the survey. Payload should be:

    {
    "user_answers": {
		  "user_ID": \<user_id\>,
		    "answers": [
		    {
		    "question": \<question id\>
		    "answer": "\<answer for this question. Any if question type is Plain Text, else can be only equal to one of question.question_answers.text. To give several answers (for multiply choice) repeat this struct with different \"answer\"\>",
		    }
		    . . .
		    ]
		    }
		    }
- \<your host url\>/api/completed-surveys/\<user id\>
- - GET method: get all surveys completed with the given user id
- \<your host url\>/api/completed-surveys/\<user id\>/\<survey id\>
- - GET method: retrieve completed with the given user id survey with the given survey id

You can use (admin - header should be with Token, exclude login method):
- \<your host url\>/api/admin/login/
- - POST method: logins you to the system and returns your token. Payload should include \"username\" and \"password\" in JSON
- \<your host url\>/api/admin/\<surveys or questions or questions-answers\>/
- - GET method: returns all surveys, questions or question-answers
- - POST method: creates new survey, question or question-answer
-  \<your host url\>/api/admin/\<surveys or questions or questions-answers\>/\<id\>/
- - GET method: retrieves survey, question or question-answer with the given id
- - PUT method: updates survey, question or question-answer with the given id using payload (look examples)
- - DELETE method: removes survey, question or question-answer with the given id 
-  \<your host url\>/api/admin/surveys/\<survey id\>/\<questions or questions-answers\>/
- - GET method: returns all questions or question-answers that belongs to the given survey
- - POST method: creates new question or question-answer that belongs to the given survey
-  \<your host url\>/api/admin/surveys/\<survey id\>/\<questions or questions-answers\>/\<id\>/
- - GET method: retrieves question or question-answer with the given id that belongs to the given survey
- - PUT method: updates  question or question-answer with the given id that belongs to the given survey using payload (look examples)
- - DELETE method: removes question or question-answer with the given id that belongs to the given survey
-  \<your host url\>/api/admin/surveys/\<survey id\>/questions/\<question id\>/questions-answers/
- - GET method: returns all question-answers that belongs to the given survey and to the given question
- - POST method: creates new question-answer that belongs to the given survey and to the given question
-  \<your host url\>/api/admin/surveys/\<survey id\>/questions/\<question id\>/questions-answers/\<id\>/
- - GET method: retrieves question-answer with the given id that belongs to the given survey and to the given question
- - PUT method: updates  question or question-answer with the given id that belongs to the given survey and to the given question using payload (look examples)
- - DELETE method: removes question or question-answer with the given id that belongs to the given survey and to the given question
-  \<your host url\>/api/admin/questions/\<question id\>/questions-answers/
- - GET method: returns all question-answers that belongs to the given question
- - POST method: creates new question-answer that belongs to the given question
-  \<your host url\>/api/admin/questions/\<question id\>/questions-answers/\<id\>/
- - GET method: retrieves question-answer with the given id that belongs to the given question
- - PUT method: updates  question or question-answer with the given id that belongs to the given question using payload (look examples)
- - DELETE method: removes question or question-answer with the given id that belongs to the given question
