# Setup Guide

1. Create a virtual environment and install dependencies:
   - `pip install -r requirements.txt`
2. Copy environment file:
   - `cp .env.example .env`
3. Run migrations:
   - `alembic upgrade head`
4. Start API:
   - `uvicorn autoops_ai.main:app --reload`
5. Run tests:
   - `pytest`
