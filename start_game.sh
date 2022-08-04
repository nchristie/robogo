docker-compose down
docker-compose build
docker-compose run --rm web python manage.py makemigrations
docker-compose run --rm web python manage.py migrate
docker-compose up
sleep 5
python3 -m webbrowser http://0.0.0.0:8000/games/