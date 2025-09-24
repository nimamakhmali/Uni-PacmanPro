# Uni-PacmanPro

## Structure

- `src/frontend/` - ui
- `src/backend/` - Api Server
- `src/ai/` - AI
- `src/shared/` - 

## Setup (Windows PowerShell)
```powershell
# 1) Create .env with your database settings (PostgreSQL)
@'
DB_HOST=127.0.0.1
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=unipacman

REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_DB=0
'@ | Out-File -Encoding utf8 .env

# 2) Install Python deps
pip install -r requirements.txt

# 3) Initialize database tables
python -m src.backend.scripts.init_db

# 4) Run API server
# uvicorn src.backend.main:app --reload --host 0.0.0.0 --port 8000
```

## Migrations (Alembic)
```powershell
# upgrade to latest
alembic upgrade head

# create a new revision (example)
alembic revision -m "add score table"

# downgrade one step
alembic downgrade -1
```

## Seed demo data
```powershell
pip install -r requirements.txt
python -m src.backend.scripts.seed_db
```

## Leaderboard queries (demo)
```powershell
python -m src.backend.scripts.leaderboard_queries
```

