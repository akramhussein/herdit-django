#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":

    settings_module = "herd.settings.%s" % os.getenv('APP_ENVIRONMENT', 'production')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
