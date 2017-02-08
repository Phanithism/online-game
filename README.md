# online-game
a simple online game website that we can play directly on browser. (like Facebook game)

### Environment ###
* Language and Framework
    * python 2.7
    * Flask 0.11

* Database
    * SQLite.


### Deployment instructions ###
1. clone this project.

2. Install python requests / urllib3.

    ```
    $ cd document-root

    $ pip install requests

    $ pip install urllib3

    $ pip install -I --user pyopenssl

    $ pip install flask_bcrypt

    $ pip install flask_login

    $ pip install peewee

    $ pip install flask_wtf

    $ pip install wtforms

    ```


### How to run Local Development ###
on python built-in server.

ref)http://flask.pocoo.org/docs/0.11/quickstart/

* command line

    ```
    $ export FLASK_APP=game.py
    $ python game.py
    ```

   access http://0.0.0.0:3030
