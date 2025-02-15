# Generated by Django 5.1.6 on 2025-02-16 09:50

import config.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('organization', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('bio', models.TextField(blank=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='persons/')),
                ('role', models.CharField(choices=[('ACTOR', 'Actor'), ('DIRECTOR', 'Director'), ('PRODUCER', 'Producer'), ('WRITER', 'Writer')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('original_title', models.CharField(blank=True, max_length=200)),
                ('description', models.TextField()),
                ('release_date', models.DateField()),
                ('duration', models.IntegerField(help_text='Duration in minutes')),
                ('rating', models.FloatField()),
                ('poster', models.ImageField(default='posters/default.jpg', upload_to='posters/')),
                ('trailer', models.FileField(upload_to='movies/trailers/', validators=[config.validators.trailer_validator, config.validators.validate_file_size])),
                ('language', models.CharField(choices=[('EN', 'English'), ('RU', 'Russian'), ('UZ', 'Uzbek'), ('KR', 'Korean'), ('TR', 'Turkish'), ('OTHER', 'Other')], max_length=10)),
                ('age_rating', models.CharField(default='PG', max_length=10)),
                ('budget', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('box_office', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('views_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('countries', models.ManyToManyField(related_name='movies', to='config.country')),
                ('genres', models.ManyToManyField(related_name='movies', to='config.genre')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('is_public', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('movies', models.ManyToManyField(related_name='collections', to='config.movie')),
            ],
        ),
        migrations.CreateModel(
            name='MovieAward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('category', models.CharField(max_length=200)),
                ('winner', models.BooleanField(default=False)),
                ('award', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.award')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='awards', to='config.movie')),
            ],
        ),
        migrations.CreateModel(
            name='MovieImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='movies/images/', validators=[config.validators.poster_validator, config.validators.validate_file_size])),
                ('is_banner', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='config.movie')),
            ],
        ),
        migrations.CreateModel(
            name='MovieReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_type', models.CharField(choices=[('BROKEN', 'Broken Video/Audio'), ('SUBTITLE', 'Subtitle Issue'), ('CONTENT', 'Inappropriate Content'), ('OTHER', 'Other Issue')], max_length=10)),
                ('description', models.TextField()),
                ('is_resolved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('resolved_at', models.DateTimeField(blank=True, null=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MovieSeason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season_number', models.IntegerField()),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('release_date', models.DateField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seasons', to='config.movie')),
            ],
            options={
                'ordering': ['season_number'],
                'unique_together': {('movie', 'season_number')},
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='MovieCast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character_name', models.CharField(max_length=200)),
                ('is_main_character', models.BooleanField(default=False)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.movie')),
                ('actor', models.ForeignKey(limit_choices_to={'role': 'ACTOR'}, on_delete=django.db.models.deletion.CASCADE, to='config.person')),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='actors',
            field=models.ManyToManyField(limit_choices_to={'role': 'ACTOR'}, related_name='acted_movies', through='config.MovieCast', to='config.person'),
        ),
        migrations.AddField(
            model_name='movie',
            name='directors',
            field=models.ManyToManyField(limit_choices_to={'role': 'DIRECTOR'}, related_name='directed_movies', to='config.person'),
        ),
        migrations.AddField(
            model_name='movie',
            name='producers',
            field=models.ManyToManyField(limit_choices_to={'role': 'PRODUCER'}, related_name='produced_movies', to='config.person'),
        ),
        migrations.AddField(
            model_name='movie',
            name='writers',
            field=models.ManyToManyField(limit_choices_to={'role': 'WRITER'}, related_name='written_movies', to='config.person'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('rating', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='config.movie')),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Subtitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=50)),
                ('subtitle_file', models.FileField(upload_to='movies/subtitles/')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subtitles', to='config.movie')),
            ],
        ),
        migrations.CreateModel(
            name='UserActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_type', models.CharField(choices=[('REVIEW', 'Added Review'), ('RATE', 'Rated Movie'), ('WATCH', 'Added to Watchlist'), ('LIKE', 'Liked Review'), ('FOLLOW', 'Followed User')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('movie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='config.movie')),
                ('review', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='config.review')),
                ('target_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='target_activities', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MovieList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_type', models.CharField(choices=[('WATCH', 'Want to Watch'), ('WATCHING', 'Currently Watching'), ('WATCHED', 'Watched'), ('FAVORITE', 'Favorites')], max_length=10)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'movie', 'list_type')},
            },
        ),
        migrations.CreateModel(
            name='MovieEpisode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('episode_number', models.IntegerField()),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('duration', models.IntegerField(help_text='Duration in minutes')),
                ('video_file', models.FileField(upload_to='movies/episodes/')),
                ('air_date', models.DateField()),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='episodes', to='config.movieseason')),
            ],
            options={
                'ordering': ['episode_number'],
                'unique_together': {('season', 'episode_number')},
            },
        ),
        migrations.AddIndex(
            model_name='movie',
            index=models.Index(fields=['title'], name='config_movi_title_a346be_idx'),
        ),
        migrations.AddIndex(
            model_name='movie',
            index=models.Index(fields=['release_date'], name='config_movi_release_160165_idx'),
        ),
        migrations.AddIndex(
            model_name='movie',
            index=models.Index(fields=['rating'], name='config_movi_rating_94410e_idx'),
        ),
        migrations.AddIndex(
            model_name='movie',
            index=models.Index(fields=['views_count'], name='config_movi_views_c_2b4a3d_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='subtitle',
            unique_together={('movie', 'language')},
        ),
        migrations.AlterUniqueTogether(
            name='watchlist',
            unique_together={('user', 'movie')},
        ),
    ]
