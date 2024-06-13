# FastAPI Template
FastAPI template with Docker, Alembic, PostgreSQL, Pytest

## Usage
```bash
pip install -e .
uvicorn --factory app.main:create_app
```

```bash
pip install -e .[test,lint]
uvicorn --factory app.main:create_app --reload
```

### Alembic commands
```bash
alembic init migrations
alembic revision --autogenerate -m "Comment"
alembic upgrade head
```

#### Notes
Run this command in psql to enable uuid_generate_v4():
- `CREATE EXTENSION IF NOT EXISTS "uuid-ossp";`
