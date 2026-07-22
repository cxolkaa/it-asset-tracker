# IT Asset Tracker

REST API for managing company IT assets — laptops, servers, monitors, software licenses, and warranty dates.

Built with **Python**, **FastAPI**, and **SQLite**. Designed as a lightweight alternative to heavy CMDB systems for small and medium IT teams.

## Features

- CRUD operations for IT assets
- Filter by status and department
- Warranty expiration alerts (`/assets/warranties/expiring`)
- Auto-generated OpenAPI documentation
- Unit tests included

## Tech Stack

| Layer      | Technology        |
|------------|-------------------|
| API        | FastAPI           |
| ORM        | SQLAlchemy        |
| Database   | SQLite            |
| Validation | Pydantic v2       |
| Tests      | pytest + httpx    |

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000/docs** for interactive API documentation.

## API Endpoints

| Method | Endpoint                        | Description                    |
|--------|---------------------------------|--------------------------------|
| GET    | `/health`                       | Health check                   |
| GET    | `/assets`                       | List assets (filterable)       |
| POST   | `/assets`                       | Create asset                   |
| GET    | `/assets/{id}`                  | Get asset by ID                |
| PATCH  | `/assets/{id}`                  | Update asset                   |
| DELETE | `/assets/{id}`                  | Delete asset                   |
| GET    | `/assets/warranties/expiring`     | Warranties expiring soon       |

## Run Tests

```bash
pytest -v
```

## License

MIT
