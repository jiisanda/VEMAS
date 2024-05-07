# VEMAS

## VEndor MAnagement System

Django Rest Framework based Vendor Management System with Performance Metrics

### Installation

1. Clone the repository

```bash
git clone https://www.github.com/jiisanda/vemas.git
```

2. Create a virtual environment

```bash
python3 -m venv venv
```

activate the virtual environment

```bash
source venv/bin/activate
```

3. Install the requirements

```bash
pip install -r requirements.txt
```

4. Setup environment variables

Sample .env file named [.env.example](.env.example) is provided in the repository. Rename the file to .env.

5. Run migrations and migrate

```bash
python manage.py makemigrations
python manage.py migrate
```

6. Runserver

```bash
python manage.py runserver
```

7. Import the postman collection to test the API

Download the postman collection from [docs/VEMAS.postman_collection.json)](docs/VEMAS.postman_collection.json).

### Problem Statement

Refer to the [Problem Statement](docs/problem_statement.md) for more details.

### API Documentation

Refer to the [API Documentation](docs/api_documentation) for more details.


