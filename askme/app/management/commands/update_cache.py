from django.core.management.base import BaseCommand
from django.core.cache import cache
from app.models import Profile, Tag


class Command(BaseCommand):
    help = 'Clear database'

    def handle(self, *args, **options):
        cache.set("popular_tags", Tag.objects.popular_tags(), 70)
        cache.set("rating_users", Profile.objects.best(), 70)
