.. image:: https://user-images.githubusercontent.com/42866208/164977163-2837836d-15bd-4a75-88fd-4e3fe2fd5dae.png
  :width: 95
  :alt: Me Logo
.. end-logo

`meapi <https://github.com/david-lev/meapi>`_: Unofficial api for 'Me - Caller ID & Spam Blocker'
##################################################################################################

.. image:: https://img.shields.io/pypi/dm/meapi?style=flat-square
    :alt: PyPI Downloads
    :target: https://pypi.org/project/meapi/

.. image:: https://badge.fury.io/py/meapi.svg
    :alt: PyPI Version
    :target: https://badge.fury.io/py/meapi

.. image:: https://www.codefactor.io/repository/github/david-lev/meapi/badge/main
   :target: https://www.codefactor.io/repository/github/david-lev/meapi/overview/main
   :alt: CodeFactor

.. image:: https://readthedocs.org/projects/meapi/badge/?version=latest&style=flat-square
   :target: https://meapi.readthedocs.io
   :alt: Docs

.. image:: https://badges.aleen42.com/src/telegram.svg
   :target: https://t.me/me_api
   :alt: Telegram

________________________

âï¸ **meapi** is a Python3 library to identify, discover and get information about phone numbers, indicate and report spam, get and manage socials, profile management and much more.

ð To **get started**, read the `Authentication guide <https://meapi.readthedocs.io/en/latest/content/setup.html>`_.

ð For a **complete documentation** of available functions, see the `Reference <https://meapi.readthedocs.io/en/latest/content/reference.html>`_.

>>ï¸ *For more information about MeÂ® -* `Click here <https://meapp.co.il/>`_.


ð Installation
--------------
.. installation

- **Install using pip3:**

.. code-block:: bash

    pip3 install -U meapi

- **Install from source:**

.. code-block:: bash

    git clone https://github.com/david-lev/meapi.git
    cd meapi && python3 setup.py install

.. end-installation

ð **Features**
---------------

ð Searching:
^^^^^^^^^^^^^

* ð Search phone numbers
* ð Get user full profile: profile picture, birthday, location, platform, socials and more
* ð« Spam indication and report

ð Social:
^^^^^^^^^^

* ð± Get user social networks: facebook, instagram, twitter, spotify and more
* âï¸ See how people call you
* ð Get mutual contacts
* ð See who watched your profile
* ð See who deleted you from his contacts book
* ð¬ Get, publish and manage comments
* ð Get users location
* ð Read app notifications

âï¸ Settings:
^^^^^^^^^^^^^

* â Change profile information
* ð¡ Configure social settings
* ð Connect social networks (And get verified blue check)
* â¬ Upload contacts and calls history
* â Block profiles and numbers
* â Delete or suspend your account


ð¨âð» **Usage**
----------------
.. code-block:: python

    from meapi import Me

    # Initialize the Client:
    me = Me(phone_number=972123456789)
    # If you have official access token:
    # me = Me(access_token='XXXXXXXX')

    # â Get information about any phone number:
    search_res = me.phone_search('+865-456-234-12')
    if search_res:
        print(search_res.name)

    # ð Get user full profile:
    if search_res.user:
        profile = search_res.get_profile()
        print(profile.email, profile.date_of_birth, profile.slogan)

        # ð± Get social media accounts:
        if profile.social.twitter.is_active:
            print(profile.social.twitter.profile_id)
            print(profile.social.twitter.posts)

    # ð¬ Watch and manage your comments:
    for comment in me.get_comments():
        print(comment.message)
        if comment.status == 'waiting':
            comment.approve()
            comment.like()

    # âï¸ Change your profile details:
    my_profile = me.get_my_profile()
    my_profile.first_name = 'David'

    # ð who watched your profile:
    for watcher in me.who_watched(incognito=True, sorted_by='last_view'):
        print(watcher.user.name, watcher.count)

    # ð¥ See how people call you:
    for group in me.get_groups():
        print(group.name, group.count)

    # â And much much more...

ð For more usage examples, read the `Examples <https://meapi.readthedocs.io/en/latest/content/examples.html>`_ page.

ð¾ **Requirements**
--------------------

- Python 3.6 or higher - https://www.python.org

ð **Setup and Usage**
-----------------------

See the `Documentation <https://meapi.readthedocs.io/>`_ for detailed instructions

â **Disclaimer**
------------------

**This application is intended for educational purposes only. Any use in professional manner or to harm anyone or any organization doesn't relate to me and can be considered as illegal.
Me name, its variations and the logo are registered trademarks of NFO LTD. I have nothing to do with the registered trademark.**

.. end-readme