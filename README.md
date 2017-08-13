# msnte_proov
This repo holds my solution to a trial excercise given to me by a company I applied
to work in. 

## Dependencies
This program uses the following Python packages:
* Flask
* Flask-RESTful
* psycopg2

They can be installed with the Python PIP package.


## Program File Descriptions
In alphabetical order:

`app_logging.py` handles all the functions necessary to configure logging to file.

`authentication.py` handles the user authentication and SQL queries related to this.

`common.py` handles values used in multiple files. It currently holds the location
for log files, and the `api_users` table mapping.

`main.py` is the main executable script. This runs the program.

`queries.py` handles the connection to the database and acts as an interface to the
database.

