# QR Code Management System

This project is a QR Code Management System that allows users to create, update, and manage QR codes. It features user registration, authentication, QR code generation with custom attributes, and relational management of QR codes and scans.

## Features

### User Management

- User registration and authentication.
- Password hashing and verification using bcrypt.

### QR Code Management

- Generate QR codes with custom attributes:
  - **URL**: Unique and required.
  - **Color**: Customizable fill color.
  - **Size**: Adjustable dimensions.
- Update existing QR codes.
- Fetch all QR codes associated with a user.

### Scans Management

- Record scans for each QR code.
- Store metadata like IP address, country, and timezone.

## Technology Stack

### Backend

- **Python**: Main programming language.
- **FastAPI**: Framework for building the API.
- **SQLAlchemy**: ORM for database interactions.

### Database

- **PostgreSQL**: Relational database for storing data.

### QR Code Generation

- **qrcode**: Python library for creating QR codes.
- **Pillow**: For image manipulation.

## Setup Instructions

### Prerequisites

1. Install Python 3.10 or higher.
2. Install PostgreSQL and create a database for the project.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/DeLaColinaSalvador/qr_challenge.git
   cd qr_challenge
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure the `.env` file:

   ```env
   DB_NAME=my_project_db
   DB_HOST=localhost
   DB_USER=user
   DB_PASSWORD=password
   SECRET_KEY=example_key_replace_this
   ```

### Running the Application

Start the development server:

```bash
uvicorn main:app --reload --port=8000
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### User Endpoints

- **POST /users/register**: Register a new user.
- **POST /users/login**: Authenticate and retrieve a JWT token.

### QR Code Endpoints

- **POST /qrcodes**: Create a new QR code.
- **PUT /qrcodes/{qr\_uuid}**: Update an existing QR code.
- **GET /qrcodes/user/{user\_uuid}**: Fetch all QR codes for a user.

### Scans Endpoints

- **POST /scans**: Record a scan for a QR code.

### Swagger Documentation

Interactive API documentation and more information on endpoint usage is available at `http://127.0.0.1:8000/docs`.

## Testing


