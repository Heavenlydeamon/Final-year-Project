# Generated manually to add XP fields to UserProfile

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0019_topic_parent_topic_topicprogress'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='xp',
            field=models.IntegerField(default=0, help_text='Current XP points'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='level',
            field=models.IntegerField(default=1, help_text='Current level based on XP'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='total_xp_earned',
            field=models.IntegerField(default=0, help_text='Total XP earned all time'),
        ),
    ]
