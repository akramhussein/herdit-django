#!/bin/bash

docker exec -it $(docker ps -aqf "name=herditdjango_app") python django/manage.py "$@"
