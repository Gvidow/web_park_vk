# Generated by Django 4.1.7 on 2023-06-13 14:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(default='default-avatar.jpg', upload_to='avatars/%Y/%m/%d/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('text', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='app.profile')),
                ('tags', models.ManyToManyField(related_name='questions', to='app.tag')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('correct', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='answers', to='app.profile')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='app.question')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('event', models.CharField(choices=[('+', 'like'), ('-', 'dislike')], max_length=1)),
                ('answer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='likes', to='app.answer')),
                ('from_whom', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='likes', to='app.profile')),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='likes', to='app.question')),
            ],
            options={
                'unique_together': {('from_whom', 'question'), ('from_whom', 'answer')},
            },
        ),
    ]
