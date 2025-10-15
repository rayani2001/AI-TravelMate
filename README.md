# 🏨 AI Hotel Booking Agent

An intelligent conversational AI agent that helps users search and book hotels using natural language. Built with OpenAI's GPT-4 and function calling capabilities.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📋 Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Docker Setup](#docker-setup)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- 🤖 **Natural Language Processing**: Chat naturally to search and book hotels
- 🔍 **Smart Search**: Filter hotels by location, price, and rating
- 📅 **Booking Management**: Create and manage reservations
- 💾 **SQLite Database**: Persistent storage for hotels and bookings
- 🌐 **Web Interface**: Beautiful Flask-based UI
- 🐳 **Docker Support**: Easy deployment with Docker
- 🛠️ **Function Calling**: Leverages OpenAI's tools API
- 📊 **Booking History**: Track all your reservations

## 🎬 Demo

```bash
You: Find me affordable hotels in New York
🤖 Agent: I found 2 hotels in New York for you:
   1. Budget Inn - $80/night (Rating: 3.8⭐)
   2. Grand Plaza Hotel - $250/night (Rating: 4.5⭐)

You: Book the Budget Inn for Alice Smith from 2025-11-15 to 2025-11-17 for 2 guests
🤖 Agent: Perfect! I've booked Budget Inn for Alice Smith.
   Check-in: November 15, 2025
   Check-out: November 17, 2025
   Guests: 2
   Total: $160 (2 nights)
   Booking ID: 1
```

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   User      │─────▶│  AI Agent    │─────▶│  Functions  │
│  (CLI/Web)  │◀─────│  (GPT-4)     │◀─────│  (Python)   │
└─────────────┘      └──────────────┘      └─────────────┘
                            │                      │
                            ▼                      ▼
                     ┌──────────────┐      ┌─────────────┐
                     │ Conversation │      │   SQLite    │
                     │   History    │      │  Database   │
                     └──────────────┘      └─────────────┘
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Git

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/hotel-booking-agent.git
cd hotel-booking-agent
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

5. **Initialize database**
```bash
python init_db.py
```

6. **Run the agent**
```bash
# CLI version
python agent.py

# Web version
python app.py
```

Visit `http://localhost:5000` for the web interface.

## 📖 Usage

### Command Line Interface

```bash
python agent.py
```

Example queries:
- "Show me all hotels in Miami"
- "Find hotels under $200 with at least 4 stars"
- "Book Grand Plaza Hotel for John Doe from 2025-12-01 to 2025-12-05 for 2 guests"
- "What are my booking details for booking ID 1?"

### Web Interface

```bash
python app.py
```

Open your browser to `http://localhost:5000` and interact with the chatbot interface.

### API Endpoints

```bash
POST /api/chat
Content-Type: application/json

{
  "message": "Find hotels in New York",
  "conversation_id": "optional-id"
}
```

## 📁 Project Structure

```
hotel-booking-agent/
│
├── agent.py              # Main AI agent logic
├── app.py                # Flask web application
├── database.py           # Database models and operations
├── init_db.py            # Database initialization script
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose setup
├── .env.example         # Environment variables template
├── README.md            # This file
│
├── static/              # Web assets
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── chat.js
│
├── templates/           # HTML templates
│   └── index.html
│
└── tests/               # Unit tests
    ├── test_agent.py
    └── test_database.py
```

## 📚 API Documentation

### Available Functions

#### `search_hotels(location, max_price, min_rating)`
Search for hotels based on criteria.

**Parameters:**
- `location` (str, required): City name
- `max_price` (float, optional): Maximum price per night
- `min_rating` (float, optional): Minimum rating (0-5)

**Returns:** List of matching hotels

#### `book_hotel(hotel_id, guest_name, check_in, check_out, num_guests)`
Create a new hotel booking.

**Parameters:**
- `hotel_id` (int, required): Hotel ID
- `guest_name` (str, required): Guest name
- `check_in` (str, required): Check-in date (YYYY-MM-DD)
- `check_out` (str, required): Check-out date (YYYY-MM-DD)
- `num_guests` (int, required): Number of guests

**Returns:** Booking confirmation with total price

#### `get_booking_details(booking_id)`
Retrieve booking information.

**Parameters:**
- `booking_id` (int, required): Booking ID

**Returns:** Booking details

#### `cancel_booking(booking_id)`
Cancel an existing booking.

**Parameters:**
- `booking_id` (int, required): Booking ID

**Returns:** Cancellation confirmation

## 🐳 Docker Setup

### Using Docker Compose (Recommended)

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Using Docker Only

```bash
# Build image
docker build -t hotel-booking-agent .

# Run container
docker run -p 5000:5000 -e OPENAI_API_KEY=your-key hotel-booking-agent
```

## 🔧 Configuration

Edit `.env` file:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4-turbo-preview

# Database
DATABASE_URL=sqlite:///bookings.db

# Flask Configuration
FLASK_ENV=development
FLASK_PORT=5000
SECRET_KEY=your-secret-key-here

# Agent Configuration
MAX_CONVERSATION_TURNS=20
ENABLE_LOGGING=true
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test
pytest tests/test_agent.py
```

## 🚀 Future Enhancements

- [ ] **Payment Integration**: Stripe/PayPal integration
- [ ] **Real Hotel APIs**: Integration with Booking.com, Expedia
- [ ] **User Authentication**: Login system with user profiles
- [ ] **Email Notifications**: Booking confirmations via email
- [ ] **Advanced Filters**: Amenities, room types, availability calendar
- [ ] **Multi-language Support**: i18n support
- [ ] **Mobile App**: React Native mobile application
- [ ] **Reviews System**: User reviews and ratings
- [ ] **Price Alerts**: Notify users of price drops
- [ ] **Loyalty Program**: Points and rewards system

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please make sure to update tests as appropriate and follow the code style guidelines.

## 📝 Code Style

This project follows PEP 8 style guidelines. Format your code using:

```bash
# Install formatters
pip install black flake8

# Format code
black .

# Check style
flake8 .
```

## 🐛 Bug Reports

Found a bug? Please open an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Environment details

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - [YourGitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- OpenAI for the GPT-4 API
- Flask community for the excellent web framework
- All contributors who helped improve this project

## 📞 Support

- 📧 Email: your.email@example.com
- 💬 Discord: [Join our server](https://discord.gg/yourserver)
- 📖 Documentation: [Read the docs](https://your-docs-url.com)

## 🔗 Links

- [Project Homepage](https://github.com/yourusername/hotel-booking-agent)
- [Issue Tracker](https://github.com/yourusername/hotel-booking-agent/issues)
- [Changelog](CHANGELOG.md)

---

Made with ❤️ by [RAYANI]

⭐ Star this repo if you find it helpful!
