# Useful Notes

Run via docker-compose using:
```
docker-compose run --rm web django-admin [django command here]
```

Migrations
```
docker-compose run --rm web python manage.py makemigrations games

docker-compose run --rm web python manage.py migrate
```

Bring up server
```
docker-compose up --rm web
docker-compose run --rm web python manage.py runserver
```

Tests
```
docker-compose run --rm web python manage.py test
```

form dir:
your_move ['__class__', '__deepcopy__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'bound_data', 'clean', 'default_error_messages', 'default_validators', 'disabled', 'empty_value', 'empty_values', 'error_messages', 'get_bound_field', 'has_changed', 'help_text', 'hidden_widget', 'initial', 'label', 'label_suffix', 'localize', 'max_length', 'min_length', 'prepare_value', 'required', 'run_validators', 'show_hidden_initial', 'strip', 'to_python', 'validate', 'validators', 'widget', 'widget_attrs']