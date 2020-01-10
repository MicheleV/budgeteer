#!/bin/sh
coverage run --omit="virtualenv/*,budgets/migrations/*,budgeteer/wsgi.py,budgets/admin*,budgets/app*,budgets/tests/*,functional_tests/*,manage.py"
manage.py test
coverage html -d coverage_html