# FastAPI Template
FastAPI template with Docker, Alembic, PostgreSQL, Pytest

## Usage
On production:
```bash
pip install uv
uv pip install -e . --system
uvicorn --factory app.main:create_app
```

On development:
```bash
pip install uv
uv venv
uv pip install -e .[test,lint]
uvicorn --factory app.main:create_app --reload
```

### Alembic commands
```bash
alembic init --template async migtaions_path
alembic revision --autogenerate -m "Init"
alembic upgrade head
```

#### Notes
Run this command in psql to enable uuid_generate_v4():
- `CREATE EXTENSION IF NOT EXISTS "uuid-ossp";`
