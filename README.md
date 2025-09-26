# Star Wars Planets API

A Django REST Framework API for managing Star Wars planets, climates, and terrains. This project provides a comprehensive CRUD API with pagination, search functionality, and external data synchronization capabilities.

## Features

- **Planet Management**: Full CRUD operations for planets with climate and terrain associations
- **Climate Management**: Manage planet climate types with search and pagination
- **Terrain Management**: Handle planet terrain types with full API support
- **Search Functionality**: Search planets, climates, and terrains by name
- **Pagination**: Configurable pagination for all list endpoints
- **External Sync**: Synchronize planet data from external SWAPI API
- **Authentication**: JWT-based authentication with read-only permissions for unauthenticated users
- **Atomic Transactions**: All write operations use database transactions for data integrity

## Technology Stack

- **Backend**: Django 4.2+
- **API Framework**: Django REST Framework 3.16+
- **Authentication**: JWT (Simple JWT)
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Filtering**: Django Filter
- **Testing**: Django Test Framework

## Installation

### Prerequisites

- Python 3.10+
- pip or uv package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd star_wars_planets
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # or with uv
   uv sync
   ```

4. **Environment configuration**
   Create a `.env` file in the project root:
   ```env
   DJANGO_SECRET_KEY=your-secret-key-here
   SWAPI_PLANETS_URL=https://swapi.dev/api/planets/
   ```

5. **Database setup**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Planets

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/planets/` | List all planets (paginated) |
| POST | `/api/planets/` | Create new planet |
| GET | `/api/planets/{id}/` | Retrieve specific planet |
| PUT | `/api/planets/{id}/` | Update planet (full) |
| PATCH | `/api/planets/{id}/` | Update planet (partial) |
| DELETE | `/api/planets/{id}/` | Delete planet |
| GET | `/api/planets/sync/` | Sync planets from SWAPI |

### Climates

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/climates/` | List all climates (paginated) |
| POST | `/api/climates/` | Create new climate |
| GET | `/api/climates/{id}/` | Retrieve specific climate |
| PUT | `/api/climates/{id}/` | Update climate (full) |
| PATCH | `/api/climates/{id}/` | Update climate (partial) |
| DELETE | `/api/climates/{id}/` | Delete climate |

### Terrains

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/terrains/` | List all terrains (paginated) |
| POST | `/api/terrains/` | Create new terrain |
| GET | `/api/terrains/{id}/` | Retrieve specific terrain |
| PUT | `/api/terrains/{id}/` | Update terrain (full) |
| PATCH | `/api/terrains/{id}/` | Update terrain (partial) |
| DELETE | `/api/terrains/{id}/` | Delete terrain |

## Query Parameters

### Pagination
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 30, max: 100)

### Search
- `search`: Search term for name fields

### Ordering
- `ordering`: Field to order by (e.g., `name`, `-population`)

### Example Requests

```bash
# List planets with pagination
GET /api/planets/?page=1&page_size=10

# Search planets by name
GET /api/planets/?search=tatooine

# Order planets by population
GET /api/planets/?ordering=-population

# Combine parameters
GET /api/planets/?search=desert&page=2&page_size=5
```

## Data Models

### Planet
- `name`: CharField (unique)
- `population`: BigIntegerField (nullable)
- `climates`: ManyToManyField to Climate
- `terrains`: ManyToManyField to Terrain
- `created_at`: DateTimeField (auto)
- `updated_at`: DateTimeField (auto)

### Climate
- `name`: CharField (unique)
- `created_at`: DateTimeField (auto)
- `updated_at`: DateTimeField (auto)

### Terrain
- `name`: CharField (unique)
- `created_at`: DateTimeField (auto)
- `updated_at`: DateTimeField (auto)

## Request/Response Examples

### Create Planet
```json
POST /api/planets/
{
  "name": "Tatooine",
  "population": "200000",
  "climates": ["arid", "hot"],
  "terrains": ["desert", "canyons"]
}
```

### Response Format
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/planets/?page=2",
  "previous": null,
  "page_size": 30,
  "total_pages": 2,
  "current_page": 1,
  "results": [
    {
      "id": 1,
      "name": "Tatooine",
      "population": "200000",
      "climates": ["arid", "hot"],
      "terrains": ["desert", "canyons"]
    }
  ]
}
```

## Authentication

The API uses JWT authentication with the following behavior:
- **Read operations** (GET): Available to all users
- **Write operations** (POST, PUT, PATCH, DELETE): Require authentication

### Getting Authentication Token

```bash
# Login to get token
POST /api/auth/login/
{
  "username": "your-username",
  "password": "your-password"
}

# Use token in requests
Authorization: Bearer <your-token>
```

## Testing

Run the test suite:

```bash
# Run all tests
python manage.py test

# Run specific test module
python manage.py test planets.tests.test_api

# Run with verbosity
python manage.py test --verbosity=2
```

### Test Coverage

The project includes comprehensive tests for:
- CRUD operations for all models
- Search functionality
- Pagination
- Authentication
- Error handling
- Data validation

## Development

### Code Style

The project follows PEP 8 standards with the following tools:
- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting

### Running Linters

```bash
# Format code
black .

# Sort imports
isort .

# Check linting
flake8
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Django secret key | Required |
| `SWAPI_PLANETS_URL` | SWAPI planets endpoint | Required for sync |
| `DEBUG` | Debug mode | False |
| `ALLOWED_HOSTS` | Allowed hosts | * |

### Settings Files

- `core/base_settings.py`: Base configuration
- `core/dev_settings.py`: Development settings
- `core/prod_settings.py`: Production settings
