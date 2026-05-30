# Swiss Agriculture Statistics API

This project is a small software application for managing and accessing Swiss agriculture statistics through a REST API.

The project contains a Flask backend, a SQLite database, and a simple Python client/demo used to test the API. The goal is to organize agricultural data such as cantons, farming categories, area types, observations, and direct payments in a clean backend structure.

## Visual Overview

### Project Architecture

![Project architecture](docs/images/architecture.png)

### Database Model Overview

![Database model overview](docs/images/database_model.png)


---

## Project Structure

```text
group-14-adoh-augustine/
│
├── backend/
│   ├── app/
│   │   └── app.py
│   │
│   ├── blueprints/
│   │   ├── areas.py
│   │   ├── cantons.py
│   │   ├── farming_categories.py
│   │   ├── observations.py
│   │   ├── direct_payment_categories.py
│   │   ├── direct_payments.py
│   │   └── legacy.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   └── data.db
│   │
│   └── services/
│
├── client/src/client
│   ├── client.py
│   └── exceptions.py
│   └── base.py
│   ├── mixins/
│   └── app_models/
│
├── proofing/
│   └── testings_demo.py
│   └── testings_clients.py
│
└── README.md
```

---

## Project Goal

The goal of this project is to build a simple backend system that can store and provide Swiss agriculture statistics through API endpoints.

The backend allows users to:

- view all cantons
- view all area types
- view all farming categories
- view agricultural observations
- filter observations
- view direct payment categories
- view direct payment observations
- test the backend through Python scripts

---

## Main Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- Pytest
- GitLab

---

## Backend Description

The backend is built with Flask and is organized using blueprints.

Each blueprint manages one part of the API:

| Blueprint | Purpose |
|---|---|
| `areas.py` | Handles agricultural area types |
| `cantons.py` | Handles Swiss cantons |
| `farming_categories.py` | Handles farming categories |
| `observations.py` | Handles agriculture statistics observations |
| `direct_payment_categories.py` | Handles direct payment categories |
| `direct_payments.py` | Handles direct payment observations |
| `legacy.py` | Contains older routes kept for compatibility |

---

## Database Models

The project uses SQLAlchemy models to represent the database tables.

Main tables:

| Table | Description |
|---|---|
| `Area` | Stores different agricultural area types |
| `Canton` | Stores Swiss cantons |
| `FarmingCategory` | Stores farming categories |
| `Observation` | Stores agriculture observation values |
| `DirectPaymentCategory` | Stores direct payment categories |
| `DirectPaymentObservation` | Stores direct payment values |

The `Observation` table connects:

- one area
- one canton
- one farming category
- one value

The `DirectPaymentObservation` table connects:

- one canton
- one direct payment category
- one value

---

## API Routes

### Basic Routes

| Method | Route | Description |
|---|---|---|
| GET | `/` | Checks if Flask is running |
| GET | `/routes` | Shows all available routes |

---

### Area Routes

| Method | Route | Description |
|---|---|---|
| GET | `/areas` | Get all area types |
| POST | `/areas` | Create a new area |
| PUT | `/areas/<id>` | Update an area |
| DELETE | `/areas/<id>` | Delete an area |

Example response:

```json
[
  {
    "area_id": 1,
    "name": "Total agricultural area"
  }
]
```

---

### Canton Routes

| Method | Route | Description |
|---|---|---|
| GET | `/cantons` | Get all cantons |

Example response:

```json
[
  {
    "canton_id": 1,
    "name": "Zurich"
  }
]
```

---

### Farming Category Routes

| Method | Route | Description |
|---|---|---|
| GET | `/categories` | Get all farming categories |

Example response:

```json
[
  {
    "category_id": 1,
    "name": "Organic farms"
  }
]
```

---

### Observation Routes

| Method | Route | Description |
|---|---|---|
| GET | `/observations` | Get all observations |
| GET | `/observations/<id>` | Get one observation |
| GET | `/observations/filter` | Filter observations |
| POST | `/observations` | Create a new observation |
| DELETE | `/observations/<id>` | Delete an observation |

Example response:

```json
[
  {
    "observation_id": 1,
    "area": "Total agricultural area",
    "canton": "Zurich",
    "category": "Organic farms",
    "value": 100.0
  }
]
```

Example filter:

```text
/observations/filter?min_value=50&max_value=200
```

---

### Direct Payment Category Routes

| Method | Route | Description |
|---|---|---|
| GET | `/direct_payment_categories` | Get all direct payment categories |
| POST | `/direct_payment_categories` | Create a new direct payment category |

---

### Direct Payment Routes

| Method | Route | Description |
|---|---|---|
| GET | `/direct_payments` | Get all direct payment observations |
| GET | `/direct_payments/<id>` | Get one direct payment observation |
| GET | `/direct_payments/filter` | Filter direct payment observations |
| POST | `/direct_payments` | Create a new direct payment observation |
| DELETE | `/direct_payments/<id>` | Delete a direct payment observation |

Example filter:

```text
/direct_payments/filter?min_value=100&max_value=1000
```

---

## Requirements

Before running the project, make sure you have installed:

- Python 3.10 or newer
- pip
- Git
- A terminal such as PowerShell, Command Prompt, Git Bash, or a Linux/macOS terminal

---

## How to Run the Project

### 1. Clone the repository

```bash
git clone <your-gitlab-repository-url>
cd group-14-adoh-augustine
```

### 2. Create a virtual environment

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

If your project has a `requirements.txt` file, use:

```bash
pip install -r requirements.txt
```

If there is no `requirements.txt` file, install the main packages manually:

```bash
pip install flask flask-sqlalchemy pytest requests
```

### 4. Start the backend

```bash
cd backend
python app/app.py
```

The backend should run on:

```text
http://127.0.0.1:5000
```

---

## How to Test the Backend

A simple pytest file can be used to check that the main routes are working.

```bash
pytest proofing/test_backend_simple.py -v
```

The tests check routes such as:

- `/`
- `/routes`
- `/areas`
- `/cantons`
- `/categories`
- `/observations`
- `/direct_payment_categories`
- `/direct_payments`

The simple tests only use `GET` requests, so they do not modify the real database.

---

## Example Test Code

```python
import pytest
import requests


BASE_URL = "http://127.0.0.1:5000"


@pytest.fixture
def api_url():
    return BASE_URL


def test_get_areas(api_url):
    response = requests.get(api_url + "/areas")
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
```

---

## Example API Usage

Using Python:

```python
import requests

response = requests.get("http://127.0.0.1:5000/areas")

print(response.status_code)
print(response.json())
```

---

## Current Features

- Flask backend
- SQLite database
- SQLAlchemy models
- Organized blueprints
- REST API routes
- Filtering for observations
- Filtering for direct payments
- Simple backend testing with pytest
- Client/demo structure

---

## Possible Future Improvements

- Add frontend interface
- Add authentication
- Add more advanced filtering
- Add pagination for large datasets
- Improve error handling
- Add more unit tests
- Add automatic database import from Excel
- Add API documentation with Swagger or Postman

---

## Authors

Software school project  
Group 14

Team members:

- Emmnauel Adoh
- Augustine collins


---

## License

This project was created for educational purposes.
