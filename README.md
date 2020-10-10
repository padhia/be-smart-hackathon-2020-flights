# flights

A sample Python application that uses Teradata database to serve flights data to users via REST API.

This application was developed as a guide for the BE SMART Hackathon 2020 participants.

## Installation
1. Install a recent version of Python (>= 3.7 recommended)
1. Clone this repository or download application files
1. Install application dependencies using: `python -m pip install -r requirements.txt`

## Running the Application
1. Update `tdconn.json` file with authentication information needed to connect to Teradata database
1. Start the application server: `python flights.py`
1. Open `http://localhost:8000/` in your browser

Following URLs are also available:
- http://localhost:8000/docs Interactive Swagger UI
- http://localhost:8000/redoc Redoc API documentation
- http://localhost:8000/openapi.json OpenAPI json specification
