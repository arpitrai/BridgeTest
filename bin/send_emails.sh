#!/usr/bin/env bash
python manage.py send_mail
python manage.py retry_deferred
