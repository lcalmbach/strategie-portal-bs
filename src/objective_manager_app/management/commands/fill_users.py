import re
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from objective_manager_app.models import Person  # Adjust the import according to your actual app and model names
import random
import string

def generate_unique_username(existing_usernames):
    """
    Generate a unique 5-character username.
    
    :param existing_usernames: List of existing usernames to ensure uniqueness.
    :return: A unique 5-character username.
    """
    while True:
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        if username not in existing_usernames:
            return username


class Command(BaseCommand):
    help = 'Create a user for each person in the Person table'

    def handle(self, *args, **kwargs):
        # self.delete_users_except_lcalm()
        self.create_users_for_persons()

    def generate_username(self, first_name, last_name):
        # Create base username from first letter of first name + first 4 letters of last name
        base_username = (first_name[0] + last_name[:4]).lower()
        username = base_username
        i = 1

        # Ensure the username is unique
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{i}"
            i += 1

        return username

    def delete_users_except_lcalm(self):
        # Delete all users except the one with username 'lcalm'
        User.objects.exclude(username='lcalm').delete()
        self.stdout.write(self.style.SUCCESS("Deleted all users except 'lcalm'"))

    def create_users_for_persons(self):
        # Fetch all persons
        persons = Person.objects.filter(user__isnull=True)
        operators_group, _ = Group.objects.get_or_create(name='operators')

        for person in persons:
            first_name = person.vorname
            last_name = person.nachname
            username = self.generate_username(first_name, last_name)

            # Create a new user
            user = User.objects.create_user(username=username, password='password')  # Set a default password
            person.user = user
            person.save()
            operators_group.user_set.add(user)    

            self.stdout.write(self.style.SUCCESS(f"Created user {username} for person {first_name} {last_name}"))
