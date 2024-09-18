from django.core.management.base import BaseCommand
from django.db import connections

class Command(BaseCommand):
    help = 'Test the database connection'

    def handle(self, *args, **kwargs):
        try:
            # Teste a conexão com o banco de dados
            with connections['default'].cursor() as cursor:
                cursor.execute("SELECT 1")
            self.stdout.write(self.style.SUCCESS('Database connection is working'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
