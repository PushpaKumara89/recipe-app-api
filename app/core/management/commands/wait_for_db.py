"""
Django management command to wait until the database is available.
"""
import time
from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait until the database is available."""

    def handle(self, *args, **options):
        """Wait until the database is available."""
        self.stdout.write("Waiting for the database...")
        db_up = False
        while not db_up:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write('Database not '
                                  'available waiting 1 second...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database available."))
