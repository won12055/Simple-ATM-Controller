# Simple ATM Controller

## Prerequisites
- Python 3.13 or higher
- Poetry for dependency management (https://python-poetry.org/docs/)

## Clone the repository
```console 
git clone https://github.com/won12055/Simple-ATM-Controller.git
```

## Install Dependencies
With Poetry installed, navigate to the project’s root directory and install the dependencies:
```console
poetry install
```

## Activate the Virtual Environment
```console
poetry shell
```

## Run the application
```console
poetry run python main.py
```

## Run tests
```console
pytest
pytest tests/test_user.py
pytest tests/test_controller.py
pytest tests/test_bank_api.py
pytest tests/test_account.py
```