# Generated by Django 4.0.1 on 2022-01-17 19:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0006_alter_userbookrelation_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_mycomment_books', to='store.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_mycomments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
