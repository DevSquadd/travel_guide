# Generated by Django 5.0.6 on 2024-07-07 08:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guide', '0004_alter_userprofile_bio'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='location',
            new_name='address',
        ),
    ]
