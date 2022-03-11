
Для запуска сервер необходимо:
1. Скачать репозиторий с кодом по ссылке. 
2. Установить docker, docker-compose на свое ПО(https://docs.docker.com/engine/install/, https://docs.docker.com/compose/install/)
3. Открыть консоль и перейти в директорию с кодом из репозитория (в корень репозитория).
4. Выполнить команды 

 docker-compose build
 docker-compose run web alembic revision --autogenerate 
 docker-compose up 

Приложение доступно по ссылке http://127.0.0.1:8000
Документация доступна по ссылке http://127.0.0.1:8000/docs

