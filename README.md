# RAG Application

A modern RAG (Retrieval-Augmented Generation) application built with FastAPI, designed to provide intelligent document processing and query capabilities.

## Features

- Document processing and embedding generation
- Intelligent query handling
- FastAPI backend with modern Python
- Docker containerization for easy deployment
- File upload and management system

## Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Git

## Quick Start

### Using Docker (Recommended)

1. Clone the repository:

```bash
git clone <repository-url>
cd RagApplication
```

2. Build and start the containers:

```bash
docker-compose up --build
```

3. Access the application at `http://localhost:8000`

### Local Development

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
uvicorn app:app --reload
```

## Project Structure

```
RagApplication/
├── app/                  # Application modules
├── uploads/             # Uploaded files storage
├── alembic/             # Database migrations
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
└── docker-compose.yml # Docker Compose configuration
```

## Environment Variables

The application requires the following environment variables:

- `COHERE_API_KEY`: Your Cohere API key for embedding generation

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

### Running Tests

```bash
# Add test commands here when tests are implemented
```

### Database Migrations

```bash
alembic upgrade head
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.
