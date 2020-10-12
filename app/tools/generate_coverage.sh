#!/bin/sh
coverage run --omit="virtualenv/*,budgets/migrations/*,budgets/admin*,budgets/app*,budgets/tests/*,budgeteer/wsgi.py,budgeteer/settings.py,functional_tests/*,manage.py,graphs/tests/*" manage.py test
coverage html -d coverage_html