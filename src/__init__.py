# Makes src/ a proper Python package so relative imports work
# both locally (uvicorn api:app run from src/) and on Render
# (uvicorn src.api:app run from project root).
