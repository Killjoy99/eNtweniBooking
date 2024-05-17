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
```bash
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
.
├── auth
│   ├── __init__.py
│   └── models.py
├── forms
│   ├── __pycache__
│   │   ├── __init__.cpython-312.pyc
│   │   ├── auth.cpython-312.pyc
│   │   └── login.cpython-312.pyc
│   ├── __init__.py
│   └── auth.py
├── services
│   ├── __pycache__
│   │   ├── __init__.cpython-312.pyc
│   │   └── authentication.cpython-312.pyc
│   ├── __init__.py
│   └── authentication.py
├── static
│   ├── bootstrap
│   │   ├── css
│   │   │   ├── bootstrap-grid.css
│   │   │   ├── bootstrap-grid.css.map
│   │   │   ├── bootstrap-grid.min.css
│   │   │   ├── bootstrap-grid.min.css.map
│   │   │   ├── bootstrap-grid.rtl.css
│   │   │   ├── bootstrap-grid.rtl.css.map
│   │   │   ├── bootstrap-grid.rtl.min.css
│   │   │   ├── bootstrap-grid.rtl.min.css.map
│   │   │   ├── bootstrap-reboot.css
│   │   │   ├── bootstrap-reboot.css.map
│   │   │   ├── bootstrap-reboot.min.css
│   │   │   ├── bootstrap-reboot.min.css.map
│   │   │   ├── bootstrap-reboot.rtl.css
│   │   │   ├── bootstrap-reboot.rtl.css.map
│   │   │   ├── bootstrap-reboot.rtl.min.css
│   │   │   ├── bootstrap-reboot.rtl.min.css.map
│   │   │   ├── bootstrap-utilities.css
│   │   │   ├── bootstrap-utilities.css.map
│   │   │   ├── bootstrap-utilities.min.css
│   │   │   ├── bootstrap-utilities.min.css.map
│   │   │   ├── bootstrap-utilities.rtl.css
│   │   │   ├── bootstrap-utilities.rtl.css.map
│   │   │   ├── bootstrap-utilities.rtl.min.css
│   │   │   ├── bootstrap-utilities.rtl.min.css.map
│   │   │   ├── bootstrap.css
│   │   │   ├── bootstrap.css.map
│   │   │   ├── bootstrap.min.css
│   │   │   ├── bootstrap.min.css.map
│   │   │   ├── bootstrap.rtl.css
│   │   │   ├── bootstrap.rtl.css.map
│   │   │   ├── bootstrap.rtl.min.css
│   │   │   └── bootstrap.rtl.min.css.map
│   │   └── js
│   │       ├── bootstrap.bundle.js
│   │       ├── bootstrap.bundle.js.map
│   │       ├── bootstrap.bundle.min.js
│   │       ├── bootstrap.bundle.min.js.map
│   │       ├── bootstrap.esm.js
│   │       ├── bootstrap.esm.js.map
│   │       ├── bootstrap.esm.min.js
│   │       ├── bootstrap.esm.min.js.map
│   │       ├── bootstrap.js
│   │       ├── bootstrap.js.map
│   │       ├── bootstrap.min.js
│   │       └── bootstrap.min.js.map
│   └── templates
│       ├── base.html
│       ├── home.html
│       ├── index.html
│       └── login.html
├── api.py
├── config.py
├── enums.py
├── exceptions.py
├── extensions.py
├── logging.py
├── main.py
├── rate_limiter.py
├── requirements.txt
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
