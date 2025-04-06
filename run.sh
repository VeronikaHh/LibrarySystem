#!/bin/bash
alembic upgrade head
python -m app.scripts.init_admin
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload