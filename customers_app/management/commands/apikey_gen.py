from django.core.management.base import BaseCommand
from rest_framework_api_key.models import APIKey

class Command(BaseCommand):
    help = 'Generate an API key'

    def handle(self, *args, **options):
        api_key, key = APIKey.objects.create_key(name="my-application-name")
        print(f"Generated API Key: {key}")
        
        # Escribe la API key en un archivo .txt en el directorio actual
        with open("./api_key.txt", "w") as f:
            f.write(key)