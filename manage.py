#!/usr/bin/env python

import sys

sys.path.append('..')

from django.conf import settings

settings.configure(INSTALLED_APPS=['sidekick'])

import django

django.setup()

from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)
