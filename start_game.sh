docker-compose down
docker-compose build
docker-compose run --rm web python manage.py makemigrations
docker-compose run --rm web python manage.py migrate

# # Comment the following line see output from console
# docker-compose up -d

# Comment the following line in order to hide output from the console
docker-compose up

sleep 5
python3 -m webbrowser http://0.0.0.0:8000/games/