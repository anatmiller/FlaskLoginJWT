# Python Simple HTTPS Server - Login Page
A login page implemented by using only Python core libs, bootstrap and jquery

Author: Liran Farage

## Technologies
* Python 3.5.2
* Jquery 3.3.1
* Bootstrap 4
* Sqlite 3
## Preconditions & Assumptions
* No sign-up page - data is pre seeded with a script.
* Registered users details is listed in `config.py`

## Usage
### 1. create/enable virtual environment
```bash
$ virtualenv -p python3 venv
$ source venv/bin/activate
```
### 2. database - create and seed
```bash
(venv)$ python db.py create seed
```
* `mydb.db` file should be created in `data/`
* to print out the data simply run `python db.py select-<table_name>` (table_name= users or sessions)
### 3. running the server 
```bash
(venv)$ python login_server.py
Enter PEM pass phrase : 1234
```
install the `security/cert.pem` file on your browser.

open your browser on `https://localhost:4443`.


## Resources
1. [Simple Python HTTP/S server](https://blog.anvileight.com/posts/simple-python-http-server/)
1. [Python web programming](http://pwp.stevecassidy.net/)
1. [python http server official docs](https://docs.python.org/3/library/http.server.html)
1. [static server in python](https://code-maven.com/static-server-in-python)
1. [sqlite in python](https://www.pythoncentral.io/introduction-to-sqlite-in-python/)
1. [Bootstrap 4](https://getbootstrap.com/docs/4.0/getting-started/introduction/)
1. [session-authentication-vs-token-authentication](https://security.stackexchange.com/questions/81756/session-authentication-vs-token-authentication)
