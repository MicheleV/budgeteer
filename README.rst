*********
Budgeteer
*********

|License| |Coverage|

- `About the project <README.rst#about-the-project>`_

  - `Built with <README.rst#built-with>`_
  
- `Getting started <README.rst#getting-started>`_

  - `Prerequisites <README.rst#prerequisites>`_
  - `Installation <README.rst#installation>`_
- `Usage <README.rst#usage>`_
- `Testing <README.rst#testing>`_
- `References and useful links <README.rst#references-and-useful-links>`_
- `Author <README.rst#author>`_
- `License <README.rst#license>`_

About the project
=================

Budgeteer is a barebone web application for managing household budgets.

Built with:
---------------------
- Python
- Django
- Bootstrap 4

Getting started
===============

Prerequisites
--------------------------
- Python 3.6 or later installed
- geckodriver in your system $PATH (needed for functional tests)

Installation
--------------------------

Clone the repo::

    git clone https://github.com/MicheleV/budgeteer

Install the requirements::

    cd app
    pip install -r requirements.txt

Gather the static files::

    cd app
    python manage.py collectstatic

Usage
=======
Run the django development server::

    cd app
    source virtualenv/bin/activate
    (virtualenv) $ python manage.py runserver [0.0.0.0:80]

Run the app using gunicorn::

    cd app
    source virtualenv/bin/activate
    (virtualenv) $ gunicorn budgeteer.wsgi:application

Run the dockerized version of the app::

    docker-composer -f docker-compose.yml up -d --build

Create and start a FedoraCoreOS VM with the dockerized version of the app::

    ./tools/prepare_fedoracoreos_containers.sh


Testing
=======

Confirm geckodriver is your $PATH::

    geckodriver --version

Install the requirements::

    cd app
    pip install -r test-requirements.txt


`Use the --keep flag to make tests faster <https://docs.djangoproject.com/en/2.2/topics/testing/overview/#the-test-database>`_

Run both function and unit test suite::

    [TEST_TARGET=localhost ] python manage.py test --keep

Run the functional test suite::

    [TEST_TARGET=localhost ] python manage.py test functional_tests --keep

Run a single functional test::

    [TEST_TARGET=localhost ] python manage.py test functional_tests.<file_name_without_py>.<class_name>.<method_name> --keep
    # e.g. python app/manage.py test functional_tests.test_base.FunctionalTest.test_expenses --keep

Run the unit test suite::

    [TEST_TARGET=localhost ] python manage.py test budgets --keep

Github is just a mirror, for the up-to-date code, issues and PR, please instead visit `the gitlab page<https://gitlab.com/micheleva>`_.

Coverage
===========================

Generate coverage::

    cd app
    ./tools/generate_coverage.sh

View it in html::

    cd app
    coverage html

References and useful links
===========================

1. `TDD with Python and Django <http://obeythetestinggoat.com/>`_

2. `Django documentation <https://docs.djangoproject.com/en/2.2/>`_

3. `Selenium documentation <https://seleniumhq.github.io/selenium/docs/api/py/api.html>`_

4. `NGINX <https://nginx.org/en/docs/>`_

5. `Ansible documentation <https://docs.ansible.com/>`_

6. `Get geckodriver <https://github.com/mozilla/geckodriver>`_

7. `Imports order convention <https://docs.openstack.org/hacking/latest/user/hacking.html#imports>`_

8. `Migrate django from sqlite3 to postgreSQL <https://web.archive.org/web/20200802014537/https://www.vphventures.com/how-to-migrate-your-django-project-from-sqlite-to-postgresql/>`_

9. `Tmp folder permissions in RHEL like distro <https://stackoverflow.com/a/33223403>`_

10. `Fedora wiki on this feature <https://fedoraproject.org/wiki/Features/ServicesPrivateTmp>`_

11. `More about it <https://serverfault.com/a/464025>`_

12. `About custom selinux policies <https://serverfault.com/a/763507/332670>`_

13. `Executing queries on init (e.g. Models.py populating dropdown) <https://stackoverflow.com/a/39084645/2535658>`_


Self-memo
=======

Backup data:
---------------------
Dump the postgres content to a file::

     docker-compose exec web sh
     # Inside the container
     pg_dump -h db -d budgeteer_db -U <db-user>  --data-only -W > data_only.sql
     # From the host
     docker cp budgeteer_web_1:/home/app/web/data_only.sql .

Restore data:
---------------------
Move the backup file to web container::

    docker cp data_only.sql budgeteer_web_1:/home/app/web/data.sql

Inject the data(execute from inside the web container, as it requires manual pwd prompt)::

    psql -h db -U budgeteer_user -d budgeteer_db < data.sql

Force gunicorn to print inside container:
---------------------
    print("<result-to-print>", flush=True)


Author
=======

Budgeteer was created by `Michele Valsecchi <https://gitlab.com/micheleva>`_


License
=======

GNU General Public License v3.0

See `COPYING <COPYING>`_ to see the full text.

.. |License| image:: https://img.shields.io/badge/license-GPL%20v3.0-brightgreen.svg
   :target: COPYING
   :alt: Repository License

.. |Coverage| image:: https://img.shields.io/badge/coverage-85%25-yellow
   :target: README.rst
   :alt: Code Coverage
