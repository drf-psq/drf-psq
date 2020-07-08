# Generated by Django 3.0.8 on 2020-07-08 22:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('libraries', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('library', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='libraries.Library')),
            ],
        ),
    ]
