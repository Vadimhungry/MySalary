start:
	poetry run python main.py

makemigration:
	poetry run alembic revision --autogenerate -m "first migration"

migrate_head:
	poetry run alembic upgrade head

app_base:
	psql postgresql://postgres:password@localhost:5432/main_backend
