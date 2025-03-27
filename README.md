# assignment-solver

TDS IITM Project2: LLM-Based Assignment Solver

## Project Name Conventions
- Must be lowercase
- Can include letters, digits, '.', '_', '-'
- Cannot contain '---'
- Maximum length: 100 characters

## Features

- Multiple file type processing:
  - CSV/Excel files
  - Log files
  - JSON data
  - SQL queries
  - Audio files
  - Image files
  
## Project Structure
```
assignment-solver/           # Root directory (renamed from Assignment_Solver)
├── requirements.txt
├── README.md
│
└── solver/
    └── tests/
        ├── test_api.py
        └── test.txt
```

## Setup

1. Clone the repository
2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

## Testing

```bash
pytest
```

## Docker Setup

```bash
docker-compose up --build
```

## API Documentation

### Endpoints

- `POST /api/assignments/` - Create new assignment
- `GET /api/assignments/` - List assignments
- `GET /api/assignments/{id}/` - Get assignment details
- `POST /api/solutions/` - Submit solution
