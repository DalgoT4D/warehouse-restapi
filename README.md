# warehouse-restapi
This repo allows Dalgo users to interface their warehouse with a set of REST apis

# FastAPI App Setup Guide

This guide provides step-by-step instructions on how to set up and run a FastAPI application, create migrations for your database, and seed initial data.

## 1. Setting Up a Python Virtual Environment

To isolate your project dependencies, it's a good practice to create a Python virtual environment. Here's how to do it:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment (Linux/macOS)
source venv/bin/activate

# Activate the virtual environment (Windows)
venv\Scripts\activate
```

## 2. Run the fastapi app

```bash
uvicorn your_app_module:app --host 0.0.0.0 --port 8005 --reload
```


## 3. Run migrations

This will create the orgs table

```bash
python migrate.py
```

## 4. Seed an org

This will create the orgs table

```bash
python seed.py --name <name of the org> --apikey <api key of the org>
```
