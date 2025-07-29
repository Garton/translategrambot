# 🌐 Telegram Translator Bot

A sophisticated universal translator bot built with **FastAPI**, **aiogram**, and **transformers**. The bot automatically detects input language, identifies target language from user prompts, and provides high-quality translations using Helsinki-NLP models.

## ✨ Features

### 🤖 Core Functionality
- **Automatic Language Detection** using `langdetect` with `lingua-language-detector` fallback
- **Smart Target Language Parsing** from user messages
- **Multi-language Support** with 50+ language pairs
- **Interactive Language Selection** via inline keyboards
- **Internationalization (i18n)** with support for multiple languages

### 🚀 Technical Features
- **Async Architecture** built with FastAPI and aiogram for high performance
- **Lightweight Translation Models** using Helsinki-NLP/opus-mt
- **CPU-Optimized** PyTorch installation (no NVIDIA dependencies)
- **Model Caching** for improved response times
- **Batch Processing** for efficient translation
- **Error Handling** with fallback translation through intermediate languages

### 🛠 Development & Deployment
- **Docker Support** with optimized containerization
- **Poetry** for dependency management
- **Comprehensive Testing** with pytest
- **Code Quality** with black, isort, and pre-commit hooks
- **Health Checks** and monitoring endpoints

## 🏗 Architecture

```
app/
├── main.py                 # FastAPI entrypoint with retry logic
├── bot.py                  # aiogram Bot & Dispatcher with custom session
├── api/routes.py           # Webhook endpoints
├── core/
│   ├── config.py          # Environment configuration
│   └── webhook.py         # Webhook registration
├── handlers/
│   ├── translate.py       # Main translation handler
│   ├── pair_select.py     # Language pair selection
│   ├── start.py          # Bot start command
│   └── admin.py          # Admin commands
├── ml/
│   ├── translation_service.py    # Helsinki-NLP translation pipeline
│   ├── language_service.py      # Language detection service
│   ├── language_parser.py       # Target language extraction
│   ├── nllb_codes.py           # Language code mappings
│   └── language_sentence_split.py # Text preprocessing
├── i18n/
│   ├── messages.py        # Internationalized messages
│   └── resources.py       # Runtime i18n strings
├── keyboards/
│   └── pairs.py          # Inline keyboard layouts
└── services/
    └── message_filter.py  # Message filtering utilities
```

## 🔧 Requirements

- **Python 3.11+**
- **Telegram Bot Token** from [@BotFather](https://t.me/botfather)
- **Docker** (optional, for containerized deployment)

## 🚀 Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/telegramTranslator.git
cd telegramTranslator

# Install dependencies
poetry install

# Configure environment
cp .env.example .env
# Edit .env with your BOT_TOKEN

# Run the bot
poetry run uvicorn app.main:app --reload
```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build manually
docker build -t telegram-translator .
docker run -p 8000:8000 telegram-translator
```

## 🌐 Webhook Configuration

The bot supports webhook mode for production deployment:

```bash
# Set webhook URL in .env
WEBHOOK_URL=https://your-domain.com/webhook

# Webhook endpoint
POST /webhook
```

For local testing, use [ngrok](https://ngrok.com) to expose your local server.

## 📊 Supported Languages

The bot supports **50+ language pairs** including:

- **European**: English, Russian, German, French, Spanish, Italian, Portuguese, Dutch, Polish
- **Asian**: Chinese, Japanese, Korean, Hindi, Thai, Vietnamese
- **Middle Eastern**: Arabic, Turkish, Hebrew, Persian
- **African**: Swahili, Amharic, Afrikaans
- **And many more...**

## 🧪 Testing

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=app

# Run specific test files
poetry run pytest tests/test_translation_service.py
```

## 🔧 Development

### Code Quality

```bash
# Format code
poetry run black app/ tests/

# Sort imports
poetry run isort app/ tests/

# Run pre-commit hooks
poetry run pre-commit run --all-files
```

### Adding New Language Pairs

1. Update `app/i18n/languages.py` with new language mappings
2. Add translations to `app/i18n/messages.py`
3. Test with `poetry run pytest tests/test_language_service.py`

## 📦 Dependencies

### Core Dependencies
- **FastAPI** (>=0.115.12) - Web framework
- **aiogram** (>=3.20.0) - Telegram Bot API
- **transformers** (>=4.52.4) - HuggingFace models
- **torch** (CPU-only) - PyTorch for inference
- **langdetect** (>=1.0.9) - Language detection
- **lingua-language-detector** (>=2.1.1) - Advanced language detection
- **spacy** (>=3.8.7) - NLP processing

### Development Dependencies
- **pytest** - Testing framework
- **black** - Code formatting
- **isort** - Import sorting
- **pre-commit** - Git hooks

## 🐳 Docker Configuration

The project includes optimized Docker configuration:

- **Multi-stage builds** for smaller images
- **CPU-only PyTorch** to avoid NVIDIA dependencies
- **Non-root user** for security
- **Health checks** for monitoring
- **Volume mounts** for model caching

## 📈 Performance

- **Model Caching**: Translation models are cached in memory
- **Batch Processing**: Multiple sentences processed together
- **Async Architecture**: Non-blocking I/O operations
- **CPU Optimization**: Lightweight models for faster inference

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the **GNU Affero General Public License v3.0** - see the [LICENSE](LICENSE) file for details.

### License Benefits
- **Copyleft Protection**: Forces derivative works to be open source
- **Network Clause**: Protects against commercial exploitation
- **Community Driven**: Ensures improvements benefit everyone
- **Commercial Friendly**: Allows you to monetize your own instance

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/telegramTranslator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/telegramTranslator/discussions)
- **Documentation**: Check the `/docs` folder for detailed guides

## 🙏 Acknowledgments

- **Helsinki-NLP** for the lightweight translation models
- **HuggingFace** for the transformers library
- **aiogram** team for the excellent Telegram Bot framework
- **FastAPI** team for the modern web framework

---

**Made with ❤️ for the open-source community**
