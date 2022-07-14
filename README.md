# robogo
Computer which plays Go, a project for Computing and Information Systems MSc at Queen Mary University

# Local development with Docker

## Initial setup / when database migrations need to take place
- Make sure you have docker installed. You can get it here if you don't yet have it: https://docs.docker.com/get-docker/
- `docker-compose build`
- `docker-compose run --rm web python manage.py makemigrations`
- `docker-compose run --rm web python manage.py migrate`
- `docker-compose up`
- Go to http://0.0.0.0:8000/games to see the server running

## Development once you've run initial setup
- Run `docker-compose up --build`
- Go to http://0.0.0.0:8000/games to see the server running

## Testing
All django-compatible tests:
- `docker-compose run --rm web python manage.py test`

One test (example):
- `docker-compose run --rm web python manage.py test games.tests.test_minimax.NodeTestCase.test_evaluate_node`

The file which isn't Django compatible:
`docker-compose run --rm web python3 -m pytest games/tests/test_game_logic.py`

## Troubleshooting
If you get this error:
`django.db.utils.OperationalError: FATAL:  the database system is starting up`
Then delete the container and image and start again. For ease here's all the initial setup in one chain:
- `docker-compose build && docker-compose run --rm web python manage.py makemigrations && docker-compose run --rm web python manage.py migrate && docker-compose up`