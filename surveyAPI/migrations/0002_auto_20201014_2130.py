# Generated by Django 2.2.10 on 2020-10-14 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surveyAPI', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('PT', 'Plain text'), ('SC', 'Single choice'), ('MC', 'Multiply choice')], max_length=2),
        ),
        migrations.AlterField(
            model_name='survey',
            name='description',
            field=models.CharField(default='No description', max_length=2048),
        ),
        migrations.AlterField(
            model_name='survey',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=128)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveyAPI.Question')),
            ],
        ),
    ]
