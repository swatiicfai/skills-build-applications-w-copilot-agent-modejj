from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta

# Ensure the `members` field is initialized as an empty list before setting its value
class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activity, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Clear existing data using raw SQL to avoid ORM issues
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM octofit_tracker_user')
            cursor.execute('DELETE FROM octofit_tracker_team')
            cursor.execute('DELETE FROM octofit_tracker_activity')
            cursor.execute('DELETE FROM octofit_tracker_leaderboard')
            cursor.execute('DELETE FROM octofit_tracker_workout')

        # Create users
        users = [
            {'username': 'thundergod', 'email': 'thundergod@mhigh.edu', 'password': 'thundergodpassword'},
            {'username': 'metalgeek', 'email': 'metalgeek@mhigh.edu', 'password': 'metalgeekpassword'},
            {'username': 'zerocool', 'email': 'zerocool@mhigh.edu', 'password': 'zerocoolpassword'},
            {'username': 'crashoverride', 'email': 'crashoverride@hmhigh.edu', 'password': 'crashoverridepassword'},
            {'username': 'sleeptoken', 'email': 'sleeptoken@mhigh.edu', 'password': 'sleeptokenpassword'},
        ]
        user_objects = [User.objects.create(**user) for user in users]

        # Create a team and initialize members as an empty list
        team = Team.objects.create(name='Blue Team')
        team.members.set([])  # Initialize as empty
        team.members.set(user_objects)  # Add members

        # Create activities
        activities = [
            {'user': user_objects[0], 'activity_type': 'Cycling', 'duration': timedelta(hours=1)},
            {'user': user_objects[1], 'activity_type': 'Crossfit', 'duration': timedelta(hours=2)},
            {'user': user_objects[2], 'activity_type': 'Running', 'duration': timedelta(hours=1, minutes=30)},
            {'user': user_objects[3], 'activity_type': 'Strength', 'duration': timedelta(minutes=30)},
            {'user': user_objects[4], 'activity_type': 'Swimming', 'duration': timedelta(hours=1, minutes=15)},
        ]
        for activity in activities:
            Activity.objects.create(**activity)

        # Create leaderboard entries
        leaderboard_entries = [
            {'user': user_objects[0], 'score': 100},
            {'user': user_objects[1], 'score': 90},
            {'user': user_objects[2], 'score': 95},
            {'user': user_objects[3], 'score': 85},
            {'user': user_objects[4], 'score': 80},
        ]
        for entry in leaderboard_entries:
            Leaderboard.objects.create(**entry)

        # Create workouts
        workouts = [
            {'name': 'Cycling Training', 'description': 'Training for a road cycling event'},
            {'name': 'Crossfit', 'description': 'Training for a crossfit competition'},
            {'name': 'Running Training', 'description': 'Training for a marathon'},
            {'name': 'Strength Training', 'description': 'Training for strength'},
            {'name': 'Swimming Training', 'description': 'Training for a swimming competition'},
        ]
        for workout in workouts:
            Workout.objects.create(**workout)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
