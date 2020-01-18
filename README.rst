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

Budgeteer is a barebone web application used to build a household budget.

Built with:
---------------------
- Python
- Django
- Selenium
- Ansible

Getting started
===============

Prerequisites
--------------------------
- Python 3.6 installed
- geckodriver in your system $PATH

Installation
--------------------------

Clone the repo::

    git clone https://github.com/MicheleV/budgeteer

Install the requirements::

    pip install -r requirements.txt

Gather the static files::
    python manage.py collectstatic

Provisioning and deploying
--------------------------

Install ansible::

    python36 -m venv virtualenv
    pip install ansible

Create your ansible inventory file inside ``tools/inventory.ansible`` ::

    [development]
    <your-server-address> ansible_become=yes ansible_ssh_user=<your-user>
    
    [staging]
    <your-other-server-address> ansible_become=yes ansible_ssh_user=<your-user>
    
    [production]
    <your-production-server-address> ansible_become=yes ansible_ssh_user=<your-user>

Install the required packages on RHEL like distros::

    cd tools
    ansible-playbook -i inventory.ansible provision.yaml [--limit=<env-name>] [--ask-become-pass]

Deploy::

    cd tools
    ansible-playbook -i inventory.ansible deploy.yaml [--limit=<env-name>] [--ask-become-pass]

Usage
=======
Run the development server::

    (virtualenv) $ python manage.py runserver [0.0.0.0:80]

Run gunicorn::

    (virtualenv) $ gunicorn budgeteer.wsgi:application


Testing
=======

Confirm geckodriver is your $PATH::

    geckodriver --version

Install the requirements::

    pip install -r test-requirements.txt

`keep option docs <https://docs.djangoproject.com/en/2.2/topics/testing/overview/#the-test-database>`_

Run both function and unit test suite::

    [TEST_TARGET=localhost ] python manage.py test --keep

Run the functional test suite::

    [TEST_TARGET=localhost ] python manage.py test functional_tests --keep

Run a single functional test::

    [TEST_TARGET=localhost ] python manage.py test functional_tests.<file_name_without_py>.<class_name>.<method_name> --keep

Run the unit test suite::

    [TEST_TARGET=localhost ] python manage.py test budgets --keep


Coverage
===========================

Generate coverage::

    ./tools/generate_coverage.sh


References and useful links
===========================

1. `TDD with Python and Django <http://obeythetestinggoat.com/>`_
2. `About custom selinux policies <https://serverfault.com/a/763507/332670>`_
3. `CentOS and nginx <https://www.digitalocean.com/community/tutorials/how-to-set-up-nginx-virtual-hosts-server-blocks-on-centos-6>`_
4. `Tmp folder permissions in RHEL like distro <https://stackoverflow.com/a/33223403>`_
    
    ...  your system probably using namespaced temporary directories, which means every 
    service can only see its own files in   /tmp.
5. `More about it <https://serverfault.com/a/464025>`_
6. `Fedora wiki on this feature <https://fedoraproject.org/wiki/Features/ServicesPrivateTmp>`_
7. `Django documentation <https://docs.djangoproject.com/en/2.2/>`_
8. `Selenium <https://seleniumhq.github.io/selenium/docs/api/py/api.html>`_
9. `Ansible <https://docs.ansible.com/>`_
10. `geckodriver <https://github.com/mozilla/geckodriver>`_
11. `Executing queries on init (e.g. Models.py populating dropdown) <https://stackoverflow.com/a/39084645/2535658>`_
12. `Imports order convention <https://docs.openstack.org/hacking/latest/user/hacking.html#imports>`_

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

.. |Coverage| image:: https://img.shields.io/badge/coverage-74%25-brightgreen
   :alt: Code Coverage
