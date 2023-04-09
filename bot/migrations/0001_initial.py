# Generated by Django 4.1.5 on 2023-03-30 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('param_name', models.CharField(max_length=255, verbose_name='Наименование параметра')),
                ('param_val', models.TextField(blank=True, null=True, verbose_name='Значение параметра')),
            ],
            options={
                'verbose_name': 'Параметр бота',
                'verbose_name_plural': 'Параметры бота',
                'ordering': ['param_name'],
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=32, null=True)),
                ('first_name', models.CharField(max_length=256)),
                ('last_name', models.CharField(blank=True, max_length=256, null=True)),
                ('language_code', models.CharField(blank=True, help_text="Telegram client's lang", max_length=8, null=True)),
                ('deep_link', models.CharField(blank=True, max_length=64, null=True)),
                ('is_blocked_bot', models.BooleanField(default=False)),
                ('is_banned', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_moderator', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Arcgis',
            fields=[
                ('location', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='bot.location')),
                ('match_addr', models.CharField(max_length=200)),
                ('long_label', models.CharField(max_length=200)),
                ('short_label', models.CharField(max_length=128)),
                ('addr_type', models.CharField(max_length=128)),
                ('location_type', models.CharField(max_length=64)),
                ('place_name', models.CharField(max_length=128)),
                ('add_num', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=128)),
                ('block', models.CharField(max_length=128)),
                ('sector', models.CharField(max_length=128)),
                ('neighborhood', models.CharField(max_length=128)),
                ('district', models.CharField(max_length=128)),
                ('city', models.CharField(max_length=64)),
                ('metro_area', models.CharField(max_length=64)),
                ('subregion', models.CharField(max_length=64)),
                ('region', models.CharField(max_length=128)),
                ('territory', models.CharField(max_length=128)),
                ('postal', models.CharField(max_length=128)),
                ('postal_ext', models.CharField(max_length=128)),
                ('country_code', models.CharField(max_length=32)),
                ('lng', models.DecimalField(decimal_places=18, max_digits=21)),
                ('lat', models.DecimalField(decimal_places=18, max_digits=21)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserActionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=128)),
                ('text', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.user')),
            ],
        ),
        migrations.AddField(
            model_name='location',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.user'),
        ),
    ]
