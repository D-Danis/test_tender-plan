
### Совет от автора

### Создать виртуальное окружение 
- python3 -m venv . venv

### Активировать виртуальное окружение 
- source .venv/bin/activate

### Установить необходимые зависимости 
- pip install -r req.txt

## Запуск Redis в Docker
- docker pull redis
- docker run -it --name redis -p 6379:6379 redis
- docker  start redis # в случае если он у вас есть

## Запуск  Celery в терминале 
- celery -A tasks worker -l info

## Запуск программы в терминале 
- python3 app.py
