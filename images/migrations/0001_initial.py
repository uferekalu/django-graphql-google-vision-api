# Generated by Django 3.1.1 on 2021-05-21 10:31

from django.db import migrations, models
import images.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(max_length=120)),
                ('image', models.ImageField(upload_to=images.models.image_upload)),
                ('labels', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'ordering': ('uuid',),
            },
        ),
    ]