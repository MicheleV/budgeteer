*********
Budgeteer
*********

|License| |Coverage|

- `About the project <README.rst#about-the-project>`_

  - `Built with <README.rst#built-with>`_
  
- `Getting started <README.rst#getting-started>`_

  - `Prerequisites <README.rst#prerequisites>`_
  - `Installation <README.rst#installation>`_
  - `Provisioning and deploying <README.rst#provisioning-and-deploying>`_
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

Getting started
===============

Prerequisites
--------------------------
- Python 3.6 installed
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

Provisioning and deploying
--------------------------

Install ansible::

    cd app
    python36 -m venv virtualenv
    pip install ansible

Create your ansible inventory file inside ``app/tools/inventory.ansible`` ::

    [development]
    <your-server-address> ansible_become=yes ansible_ssh_user=<your-user>
    
    [staging]
    <your-other-server-address> ansible_become=yes ansible_ssh_user=<your-user>
    
    [production]
    <your-production-server-address> ansible_become=yes ansible_ssh_user=<your-user>

Provision (on RHEL like distros)::

    cd app/tools
    ansible-playbook -i inventory.ansible provision.yaml [--limit=<env-name>] [--ask-become-pass]

Deploy::

    cd app/tools
    ansible-playbook -i inventory.ansible deploy.yaml [--limit=<env-name>] [--ask-become-pass]

Usage
=======
Run the development server::

    cd app
    source virtualenv/bin/activate
    (virtualenv) $ python manage.py runserver [0.0.0.0:80]

Run gunicorn::

    cd app
    source virtualenv/bin/activate
    (virtualenv) $ gunicorn budgeteer.wsgi:application

Run the dockerized version::

    docker-composer -f docker-compose.yml up -d --build


Testing
=======

Confirm geckodriver is your $PATH::

    geckodriver --version

Install the requirements::

    cd app
    pip install -r test-requirements.txt

`keep option docs <https://docs.djangoproject.com/en/2.2/topics/testing/overview/#the-test-database>`_

Run both function and unit test suite::

    [TEST_TARGET=localhost ] python manage.py test --keep

Run the functional test suite::

    [TEST_TARGET=localhost ] python manage.py test functional_tests --keep

Run a single functional test::

    [TEST_TARGET=localhost ] python manage.py test functional_tests.<file_name_without_py>.<class_name>.<method_name> --keep
    # Example: python app/manage.py test functional_tests.test_base.FunctionalTest.test_expenses --keep

Run the unit test suite::

    [TEST_TARGET=localhost ] python manage.py test budgets --keep


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
2. `About custom selinux policies <https://serverfault.com/a/763507/332670>`_
# replace nginx link with nginx official docs
# change link order
3. `CentOS and nginx <https://www.digitalocean.com/community/tutorials/how-to-set-up-nginx-virtual-hosts-server-blocks-on-centos-6>`_
4. `Tmp folder permissions in RHEL like distro <https://stackoverflow.com/a/33223403>`_
5. `More about it <https://serverfault.com/a/464025>`_
6. `Fedora wiki on this feature <https://fedoraproject.org/wiki/Features/ServicesPrivateTmp>`_
7. `Django documentation <https://docs.djangoproject.com/en/2.2/>`_
8. `Selenium documentation <https://seleniumhq.github.io/selenium/docs/api/py/api.html>`_
9. `Ansible documentation <https://docs.ansible.com/>`_
10. `Get geckodriver <https://github.com/mozilla/geckodriver>`_
11. `Executing queries on init (e.g. Models.py populating dropdown) <https://stackoverflow.com/a/39084645/2535658>`_
12. `Imports order convention <https://docs.openstack.org/hacking/latest/user/hacking.html#imports>`_
13. `Migrate django from sqlite3 to postgreSQL <https://web.archive.org/web/20200802014537/https://www.vphventures.com/how-to-migrate-your-django-project-from-sqlite-to-postgresql/>`_

Self-memo
=======

Backup data:
---------------------
Dump the postgres content to a file::
     docker exec -it --user root  budgeteer_web_1 pg_dump -h db -d budgeteer_db -U <db-user>  --data-only -W > data_only.sql
     docker cp budgeteer_web_1:/home/app/web/data_only.sql .

Restore data:
---------------------
Move the backup file to web container::
    docker cp data_only.sql budgeteer_web_1:/home/app/web/data.sql

Inject the data(execute from inside the web container)::
    psql -h db -U budgeteer_user -d budgeteer_db < data.sql


Inspect data with GUI:
---------------------
GUI postgre editor::
    docker pull dpage/pgadmin4
    sudo docker run --rm -d --network budgeteer_default  --name pgadmin4 -p 5050:80 --env PGADMIN_DEFAULT_EMAIL=admin@example.com --env PGADMIN_DEFAULT_PASSWORD=<super-safe-password>  dpage/pgadmin4

Author
=======

Budgeteer was created by `Michele Valsecchi <https://github.com/MicheleV>`_


License
=======

GNU General Public License v3.0

See `COPYING <COPYING>`_ to see the full text.

.. |License| image:: https://img.shields.io/badge/license-GPL%20v3.0-brightgreen.svg
   :target: COPYING
   :alt: Repository License

.. |Coverage| image:: https://img.shields.io/badge/coverage-78%25-yellow
   :alt: Code Coverage
