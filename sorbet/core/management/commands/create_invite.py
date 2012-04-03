from django.core.management.base import BaseCommand, CommandError
from sorbet.core.models import Invitation

class Command(BaseCommand):
    args = ''
    help = 'Create a brand new invitation key'

    def handle(self, *args, **options):
        key = Invitation.objects.create()
        self.stdout.write("A brand new invitation key for you, perv: %s\n" % key.key)
