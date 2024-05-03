# Digital Skills | Child performance tracking service

[![ru](https://img.shields.io/badge/lang-ru-green.svg)](README.ru.md)
[![en](https://img.shields.io/badge/lang-en-red.svg)](README.md)
___

1. [Project Objective](#project-objective)
2. [Realization](#realization)
    + [Technical part](#technical-part)
    + [Business tasks](#business-tasks)
3. [Project Structure](#project-structure)
4. [Description of environment variables](#description-of-environment-variables)
5. [Launch](#launch)
    + [Requirements](#requirements)
    + [Start local development server](#start-local-development-server)

___

## Project Objective

The service is aimed at tracking the child's progress in various events and
educational institutions.

The capabilities of this service:
- The organization that held the event can record the results for each participant.
- A parent can see the activity of their children at the events they have completed.

## Realization

___

### Technical Part

* The web application is implemented using [Flask](https://flask.palletsprojects.com/en/2.3.x/).
* PostgreSQL is used as the main DBMS.
* [SQLAlchemy](https://www.sqlalchemy.org/) ORM is used to interact with the database.
* JWT is used for authorization and authentication.
* Sending emails using SMTP (gmail).

### Business tasks

* Two types of registration are implemented - for the parent and the organization.
* Users can change their password in their personal account.
* Parents can add a child to track statistics on him.
* An organization can create, edit, or delete an event.
* The organization can specify achievements for each event.
* A parent can send a request to register a child for an event.
* The organization can accept or reject the application.
* An organization can assign achievements for an event to a child.
* The parent can see the child's entire academic performance on a separate page.

## Project Structure

___

- `docs` - Project documentation.
- `portfolio` - Web-application.
    - `bootstrap` - Bootstrap data when the application is launched.
    - `configs` - Web Application configuration.
    - `drivers` - Drivers (servers) used in the web application.
    - `enums` - Enums (including errors).
    - `internal`
        - `biz` - Business logic of a web application.
            - `dao` - DAO layer.
            - `deserializers` - Data deserialization.
            - `serializers` - Data serialization.
            - `services` - Services provided by business logic.
            - `validators` - Data validation.
        - `http` - Web Application API.
    - `models` - Web Application Models.
    - `templates` - Web Application Templates.
    - `.env.example` - Example of an environment variable file.
    - `main.py` - Script for launching a web application.
    - `requirements.txt` - Main dependencies of web-application.
    - `setup.py` - A script for preparing a web application.

## Description of environment variables

___

* `HTTP_HOST` - Host on which the web application will be running.
* `HTTP_PORT` - Port on which the web application will be running.
* `DEBUG` - Debug mode (0 or 1).
* `DB_HOST` - Host on which the database is running.
* `DB_PORT` - Port on which the database is running.
* `DB_USER` - Database user.
* `DB_PASSWORD` - Password for the database user.
* `DB_NAME` - Name of the database.
* `MAIL_HOST` - Host on which SMTP server is running.
* `MAIL_PORT` - Port on which SMTP server is running.
* `MAIL_FROM` - email - SMTP server user.
* `MAIL_PASSWORD` - The password for the SMTP server user.
* `SECRET_KEY_SESSION` - The secret key of the session.
* `SECRET_KEY` - The secret key of the web application.
* `ENCRYPT_ALGORITHM` - Алгоритм шифрования (JWT).
* `LIFETIME_CODE` - The lifetime of the account verification code.
* `SEND_CODE_INTERVAL` - The time required to be able to resend 
  the account verification code.

## Launch

___

### Requirements

* Installed python `3.8`.
* Make sure that the following services are installed and running:
    * `postgresql`

### Start local development server

1. Create a PostgreSQL database to be used in the project.
2. Create `portfolio/.env` file and specify the environment variables by example `portfolio/.env.example`.
3. `python3 -m venv venv` - Create a virtual environment.
4. `source venv/bin/activate` - Activate the virtual environment.
5. `pip3 install -r requirements.txt` - Install dependencies.
6. `python setup.py` - Run the project preparation script.
7. You are already to start!
   To start the local server, run the following command:
   ```shell
   python main.py
   ```
   If you specified `HTTP_HOST=0.0.0.0`, `HTTP_PORT=8000`,
   your local server will be available via the link [http://0.0.0.0:8000](http://0.0.0.0:8000)
