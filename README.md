# `eNtweniBooking`

A booking API with ride hailing and food delivery microservices.

## `Tech Stack`

    Python
    FastAPI
    Kivy/Kivymd

### `Requirements`

Requirements are found in the respective folders i.e `backend/requirements.txt` and `frontend/requirements.txt`

## `Development`

These are the development steps for both the frontend and the backend

### `Frontend`

`Linux`
```sh
    cd frontend/
    python -m venv venv
    source venv/bin/activate # activate the virtual environment
    pip install -r requirements.txt
    python main.py          # run the frontend app
```

`Windows`

    cd frontend/
    python -m venv venv
    .\venv\Scripts\activate.bat # activate the virtual environment
    pip install -r requirements.txt
    python main.py          # run the frontend app

### `Backend`

> The Folder Structure follows the netflix-dispatch fomular for fastapi apps. this is a robust structure that allows for exponential growth of the api without issues.

```sh
ENTWENIBOOKING/backend
├── auth
│   ├── __init__.py
│   ├── models.py
│   ├── permissions.py
│   ├── routers.py
│   └── service.py
├── common
│   ├── utils
│   │   ├── __init__.py
│   │   ├── cli.py
│   │   └── views.py
│   ├── __init__.py
│   └── managers.py
├── database
│   └── __init__.py
├── forms
│   └── __init__.py
├── notification
│   ├── __init__.py
│   ├── models.py
│   ├── routers.py
│   └── service.py
├── organisation
│   ├── __init__.py
│   ├── models.py
│   ├── routers.py
│   └── service.py
├── plugin
│   ├── __init__.py
│   ├── models.py
│   ├── routers.py
│   └── service.py
├── plugins
│   └── __init__.py
├── product
│   ├── __init__.py
│   ├── models.py
│   ├── routers.py
│   └── service.py
├── static
│   ├── bootstrap
│   │   ├── css
│   │   │   └── bootstrap.min.css
│   │   └── js
│   │       └── bootstrap.min.js
│   └── templates
│       ├── base.html.j2
│       ├── home.html.j2
│       ├── index.html.j2
│       └── login.html.j2
├── api.py
├── config.py
├── decorators.py
├── enums.py
├── exceptions.py
├── logging.py
├── main.py
├── models.py
├── rate_limiter.py
├── requirements.txt
├── run.py
├── scheduler.py
└── server-config.json
```

`Linux`

```bash
cd backend/
python -m venv backend
source venv/bin/activate # activate the virtual environment
pip install -r requirements.txt
python -m uvicorn main:app --reload          # run the backend app
```

`Windows`

    cd backend/
    python -m venv backend
    source venv/bin/activate # activate the virtual environment
    pip install -r requirements.txt
    python -m uvicorn main:app --reload          # run the backend app

`Bootstrap`

    Download bootstrap 5 and extact it to the static folder.
    Rename the folder bootstrap

## `Deployment`

On production we will be using Nginx Unit

1. Json Configuaration

```json
{
    "listeners": {
        "*:80": {
            "pass": "applications/eNtweniBooking"
        }
    },
    "applications": {
        "eNtweniBooking": {
            "type": "python3",
            "path": "/app",
            "home": "/media/serpent99/Code/Python/APIs/eNtweniBooking/backend",
            "module": "api",
            "callable": "app"
        }
    }
    
}
```

2. start the server

```sh
sudo unitd
```

3. Give unit access to the folder

```sh
sudo chown unit:unit .
```

3. Push the config to the server

```sh
sudo curl -X PUT --data-binary @server-config.json --unix-socket /var/run/control.unit.sock http://localhost/config
```

4. If pushing fails, get the current config with

```sh
sudo curl -X GET --data-binary @server-config.json --unix-socket /var/run/control.unit.sock http://localhost/config
```

The backend server will be deployed using `Nginx Unit`, an Nginx server built to deploy multiple web apps on the same server with just different port access.

## `Contributing`

Contributions to the eNtweni Booking API are welcome and will be closely examined by lead devs before integration.
If you cannot contribute with writing code, kindly star the project and your efforts will not be taken for granted.
Thank you for supporting `eNtweni Team`
