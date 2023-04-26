# User authentication using FastAPI, MongoDB, Docker Compose
## How to start the application

**The commands:**

First you have to git clone the files by entering in your terminal:
```
$ git clone https://github.com/IvanYukish/fast_api_tech_task.git
```  
Then create a .env file
```
cp .env.example .env
```

Then start the application:
```
$ docker-compose up -d
```
The above command will both create the images and start the containers (2 images and 2 containers—one for the FastAPI application and one for the MongoDB database).

## Running tests:
[test_main.http](test_main.http) contains a typical test cases for our application.
If you are using pycharm you can simply click on green-run button.

![Screenshot from 2023-04-26 22-08-08.png](..%2F..%2FPictures%2FScreenshot%20from%202023-04-26%2022-08-08.png)

## Application description

For visualizing the application, open up your browser and enter:

* http://0.0.0.0:8000/#/

In the application we have seven sections:
* For authentication (the right green "Authorize" button from the above);
* For creating users (3 roles are acceptable only: "admin", "dev", "simple mortal", you'll see an error if not respecting the rule);
* For creating tokens by entering user's credentials;
* For listing the users;
* For watching the current user (only if authenticated);
* For modifying user properties (only if authenticated with admin role);
* For deleting the user.

To see the running containers in docker, enter in the terminal:
```
$ docker ps
```
To see the database and collection created (database name is: mongo_tech, collection: users) enter in your terminal:
```
$ docker exec -it <mongo-container-id> bash
$ mongosh

```

## Configuration and file structure
Our file structure is:
```
.
├── app
│ ├── core
│      ├── schemas.py
│      ├── middleware.py
│      ├── db.py
│ ├── user
│      ├── constants.py
│      ├──__init__.py
│      ├──dependencies.py
│      ├──enums.py
│      ├──schemas.py
│ ├── v1
│      ├──router.py
│      ├──user.py
│ ├── config.py
│── test_main.http
│── pyproject.toml
│── poetry.lock
│── main.py
│── Dockerfile
│──docker-compose.yml
│──.gitignore
│──.env.example
│──.dockerignore
└── .env

```
In the app directory in [main.py](main.py) file we make all the dependencies and routers importing from the same name files located in ```app``` directory.

[app](app) directory is the one that contains all the needed schemas models ([schemas.py](app%2Fuser%2Fschemas.py)), database and authentication variables (settings.py). 

Authentication is made by using ```bearer``` scheme with ```token``` creation and usage.

[dependencies.py](app%2Fuser%2Fdependencies.py) is the file containing authentication functions (I also made an authentication middleware located in ```main.py``` file in the root directory using ```basic``` scheme, this function serves as an example purpose only).