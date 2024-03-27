## app/core/management/commands/wait_for_db.py

# 장고 어드민 코드가 동작하는 곳
# 장고가 디피 연결에 실패했을 시, 재시도를 하도록 만드는 로직 추가
# 여기서의 장고는 도커에서의 장고라 로컬에서는 인식이 안됌! 나중에 다 됩니다...

from django.db import connections
import time
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as Psycopg2OpError


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Waiting for DB Connections...") # command로 로그 노출

        is_db_connected = None

        while not is_db_connected: # DB 연결에 성공할 때까지 시도
            try:
                is_db_connected = connections['default'] # settings.py에 있는 DATABASE의 default = postgresql
            except(OperationalError, Psycopg2OpError):
                self.stdout.write("Retrying DB connection ...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('PostgreSQL Connections Success'))
