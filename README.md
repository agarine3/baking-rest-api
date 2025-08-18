# 🏦 Banking REST API

A complete banking system built with FastAPI, SQLAlchemy, and JWT authentication. This project demonstrates AI-driven development practices to create a production-ready banking API in just 1 hour.

## 🎬 Demo Video

**Demo Video Link:** [Add your video link here]
- Complete walkthrough of all banking features
- Authentication, account management, transactions, cards, and statements
- Edge cases and security demonstrations
- API documentation showcase

## 🚀 Features

### Core Banking Services
- ✅ **User Authentication** - JWT-based secure authentication
- ✅ **Account Management** - Create, list, and manage bank accounts
- ✅ **Transaction Processing** - Deposits, withdrawals, and transfers
- ✅ **Card Management** - Issue and manage debit/credit cards
- ✅ **Statement Generation** - Monthly account statements
- ✅ **Security** - Password hashing, authorization, validation

### Technical Features
- ✅ **FastAPI** - Modern, fast web framework with automatic documentation
- ✅ **SQLAlchemy ORM** - Database abstraction with proper relationships
- ✅ **SQLite Database** - File-based database for development
- ✅ **JWT Authentication** - Secure token-based authentication
- ✅ **Pydantic Validation** - Request/response data validation
- ✅ **Alembic Migrations** - Database schema management
- ✅ **Comprehensive Testing** - Unit tests for critical functionality
- ✅ **CORS Support** - Cross-origin resource sharing
- ✅ **Error Handling** - Proper HTTP status codes and error messages

## 🛠️ Technology Stack

- **Backend Framework:** FastAPI
- **Database ORM:** SQLAlchemy
- **Database:** SQLite
- **Authentication:** JWT (JSON Web Tokens)
- **Password Hashing:** bcrypt
- **Data Validation:** Pydantic
- **Database Migrations:** Alembic
- **Testing:** pytest
- **Documentation:** Auto-generated OpenAPI/Swagger

## 📋 Requirements Coverage

### ✅ Service Interface
- [x] User Signing up
- [x] Authentication (JWT)
- [x] Account Holders management
- [x] Accounts creation and management
- [x] Transactions (deposits, withdrawals)
- [x] Money Transfer between accounts
- [x] Cards issuance and management
- [x] Statements generation

### ✅ Database Implementation
- [x] SQLite database with proper schema
- [x] SQLAlchemy ORM with relationships
- [x] Alembic migrations for schema management
- [x] Data validation and constraints

### ✅ Security Features
- [x] JWT token authentication
- [x] Password hashing with bcrypt
- [x] Account ownership validation
- [x] Transaction limits and validation
- [x] Input data validation

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/agarine3/baking-rest-api.git
cd baking-rest-api
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp env.example .env
# Edit .env with your configuration
```

4. **Run database migrations**
```bash
alembic upgrade head
```

5. **Start the server**
```bash
uvicorn app.main:app --reload --port 8000
```

6. **Access the API**
- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **Demo UI:** http://localhost:8080 (after starting demo server)

### Demo UI Setup
```bash
cd demo
python3 -m http.server 8080
```

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/v1/auth/signup` - Register new user
- `POST /api/v1/auth/login` - Authenticate user

### Account Endpoints
- `POST /api/v1/accounts/` - Create new account
- `GET /api/v1/accounts/` - List user accounts
- `GET /api/v1/accounts/{id}` - Get account details

### Transaction Endpoints
- `POST /api/v1/transactions/` - Create transaction
- `POST /api/v1/transactions/transfer` - Transfer money
- `GET /api/v1/transactions/account/{id}` - List account transactions

### Card Endpoints
- `POST /api/v1/cards/` - Issue new card
- `GET /api/v1/cards/` - List user cards
- `PATCH /api/v1/cards/{id}/status` - Update card status

### Statement Endpoints
- `POST /api/v1/statements/generate` - Generate statement
- `GET /api/v1/statements/account/{id}` - List account statements

## 🧪 Testing

Run the test suite:
```bash
pytest
```

Run specific tests:
```bash
pytest tests/test_basic.py
pytest tests/test_models_simple.py
```

## 📁 Project Structure

```
banking-rest-api/
├── app/
│   ├── api/                 # API endpoints
│   │   ├── auth.py         # Authentication endpoints
│   │   ├── accounts.py     # Account management
│   │   ├── transactions.py # Transaction processing
│   │   ├── cards.py        # Card management
│   │   └── statements.py   # Statement generation
│   ├── core/               # Core functionality
│   │   ├── auth.py         # JWT authentication
│   │   └── security.py     # Password hashing
│   ├── models/             # SQLAlchemy models
│   │   ├── user.py         # User model
│   │   ├── account.py      # Account model
│   │   ├── transaction.py  # Transaction model
│   │   ├── card.py         # Card model
│   │   └── statement.py    # Statement model
│   ├── schemas/            # Pydantic schemas
│   │   ├── auth.py         # Auth request/response
│   │   ├── account.py      # Account schemas
│   │   ├── transaction.py  # Transaction schemas
│   │   ├── card.py         # Card schemas
│   │   └── statement.py    # Statement schemas
│   ├── config.py           # Configuration settings
│   ├── database.py         # Database connection
│   └── main.py             # FastAPI application
├── alembic/                # Database migrations
├── demo/                   # Demo UI
│   └── index.html          # Interactive demo interface
├── tests/                  # Test files
├── requirements.txt        # Python dependencies
├── env.example            # Environment variables template
├── AI_USAGE_LOG.md        # AI development log
└── README.md              # Project documentation
```

## 🔐 Security Considerations

### Authentication & Authorization
- JWT tokens with 30-minute expiration
- Secure password hashing with bcrypt
- Account ownership validation
- User activity tracking

### Data Validation
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy
- XSS protection with proper response handling
- CORS configuration for frontend integration

### Business Logic Security
- Transaction amount validation
- Daily/monthly limit enforcement
- Insufficient funds prevention
- Account status validation

## 🤖 AI-Driven Development

This project was built using AI-assisted development practices:

### AI Tools Used
- **Cursor IDE** - AI-powered code editor
- **Claude** - Code generation and debugging
- **ChatGPT** - Problem solving and architecture
- **Various AI Tools** - Iterative development

### Development Process
1. **Repository Setup** - AI-assisted project structure
2. **Database Design** - AI-generated SQLAlchemy models
3. **API Development** - AI-assisted endpoint implementation
4. **Testing** - AI-generated test cases
5. **Documentation** - AI-assisted documentation
6. **Demo Creation** - AI-generated demo interface

### Challenges & Solutions
- **Dependency Management** - Resolved Python package compatibility
- **Database Relationships** - Fixed SQLAlchemy foreign key issues
- **API-Schema Alignment** - Synchronized Pydantic and SQLAlchemy models
- **Error Handling** - Comprehensive validation and error responses

## 📊 Performance & Scalability

### Current Implementation
- SQLite database for development
- FastAPI with async support
- Efficient ORM queries
- Proper indexing on foreign keys

### Production Considerations
- PostgreSQL for production database
- Redis for caching
- Load balancing for high traffic
- Database connection pooling
- API rate limiting

## 🎯 Future Enhancements

### Planned Features
- [ ] Multi-currency support
- [ ] International transfers
- [ ] Mobile app API
- [ ] Webhook notifications
- [ ] Advanced fraud detection
- [ ] Real-time transaction monitoring

### Technical Improvements
- [ ] GraphQL API
- [ ] Microservices architecture
- [ ] Event-driven architecture
- [ ] Advanced caching strategies
- [ ] Comprehensive logging
- [ ] Performance monitoring

## 📞 Support

For questions or issues:
- **Repository:** https://github.com/agarine3/baking-rest-api
- **Issues:** Create an issue on GitHub
- **Documentation:** http://localhost:8000/docs (when running)

## 📄 License

This project is created for demonstration purposes as part of an AI-driven development assessment.

---