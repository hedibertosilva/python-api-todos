# API TODOS

![Flask](https://img.shields.io/static/v1?style=for-the-badge&logo=flask&logoColor=white&label=flask&message=2.1&color=blue)
![Python](https://img.shields.io/static/v1?style=for-the-badge&logo=python&logoColor=white&label=python&message=3.9&color=blue)

This application collect and process 3rd-party data from external source, specially from `https://jsonplaceholder.typicode.com/todos`.

The project was designed as a loosely coupled system that accepts serveral different data sources that follow our abstract interface, watching and expecting pre-registered data keys in the tasks (like id and title). 

## Prerequisites

Before you begin, ensure you have met the following requirements:
* You have installed the version of Python between v3.7 and v3.9 (JWT module still doesn't work in Python 3.10). 
* You have installed the latest version of Pip.
*  deployment with virtualenv, you have installed the latest version of virtualenv (pip module).
* For deployment with Docker, you have installed the version of Docker >= v20. 
* For deployment with Docker, you have installed the version of Docker-compose >= v1.28. 
* For testing, you have installed the lastest version of Tox (pip module).

## Installing

After clone the project, follows this steps to deploy:

#### Using Docker (recommended)

Before running the command, make sure you have a free port 5000 on the host. If not, you must change the published port on the docker-compose file inside the docker directory.

``` console
  docker-compose -f docker/docker-compose.yml up -d --build
```
If you prefer to use a docker stack, ensuring that you already init the swarm, use:
``` console
  docker stack deploy -c docker/docker-compose.yml api-todos
```

#### Using Virtual Environment

Before running the command, make sure you have a free port 5000 on the host. If not, you must change the published port variable on the `run.sh` file in the root project path.  

``` console
  chmod +x run.sh
```
``` console
  sh run.sh
```

## Usage

The application uses JWT module to ensure system security, so you must login to get the Bearer Token before list the TODO tasks. 

The admin user (pre-registered user) can be defined on environment variables in the install step (`docker-compose.yml` or `run.sh`).

### Login

`POST /v1/login/`

``` console
curl --location --request POST 'http://127.0.0.1:5000/v1/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "admin",
    "password": "admin"
}'
```

##### Response

    HTTP/1.1 201 Created
    Status: 201 Created
    Content-Type: application/json
    Content-Length: 330

``` json
{
    "data": {
        "expires_at": "",
        "token": "",
        "user": {
            "created_at": "",
            "id": 1
        }
    },
    "message": "The token was generated successfully."
}
```
### 

### Sing up

`POST /v1/users/`

``` console
curl --location --request POST 'http://127.0.0.1:5000/v1/users' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "hediberto",
    "password": "silva"
}'
```

##### Response

    HTTP/1.1 201 Created
    Status: 201 Created
    Content-Type: application/json
    Content-Length: 141

``` json
{
    "data": {
        "created_at": "",
        "id": 2,
        "username": "hediberto"
    },
    "message": "The user has been successfully registered."
}
```
### 

### Listing TODO tasks.

For listing the tasks, use the Bearer Token from login route on the Authorization Header. The number of tasks returned is defined by query string limit. The default limit is 5.

`GET /v1/todos/`

**Args:**
- **limit:** defaults to 5.

``` console
curl --location --request GET 'http://127.0.0.1:5000/v1/todos' \
--header 'Authorization: Bearer XXXXX'
```

##### Response

    HTTP/1.1 200 OK
    Status: 200 OK
    Content-Type: application/json
    Content-Length: 252

``` json
[
    {
        "id": 1,
        "title": "delectus aut autem"
    },
    {
        "id": 2,
        "title": "quis ut nam facilis et officia qui"
    },
    {
        "id": 3,
        "title": "fugiat veniam minus"
    },
    {
        "id": 4,
        "title": "et porro tempora"
    },
    {
        "id": 5,
        "title": "laboriosam mollitia et enim quasi adipisci quia provident illum"
    }
]
```

``` console
curl --location --request GET 'http://127.0.0.1:5000/v1/todos?limit=1' \
--header 'Authorization: Bearer XXXXX'
```

##### Response

    HTTP/1.1 201 Created
    Status: 201 Created
    Content-Type: application/json
    Content-Length: 141

``` json
[{
    "id":1,
    "title":"delectus aut autem"
}]
```

## Testing

For tests and coverage, use:

``` console
 tox -r -e coverage
```

For Pep8 test, use:

``` console
 tox -r -e pep8
```

## CI (only on GitLab)

Use `.gitlab-ci.yml` file.

## Contact

If you want to contact me you can reach me at hed.cavalcante@gmail.com.

## License

This project uses the following license: GNU v3.0.
