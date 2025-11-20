# System Monitor 🖥️

A Python-based system monitoring tool that captures screenshots and sends email notifications.

## Features

- 📸 **Automated Screenshots**: Capture multi-monitor screenshots organized by hostname and date
- 📧 **Email Notifications**: Send system alerts via SMTP with robust error handling
- 🔧 **Configurable**: Environment-based configuration with `.env` support
- 📝 **Logging**: Comprehensive logging for monitoring and debugging
- 🛡️ **Error Handling**: Graceful error recovery with detailed logging

## Project Structure

```
system_monitor/
├── config/
│   └── settings.py          # Configuration management
├── services/
│   ├── email_service.py     # Email sending functionality
│   └── screenshot_service.py # Screenshot capture
├── utils/
│   ├── paths_utils.py       # Path utilities
│   └── time_utils.py        # Time formatting utilities
├── main.py                  # Application entry point
├── .env.example             # Environment variables template
└── requirements.txt         # Python dependencies
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/msicse/system_monitor.git
cd system_monitor
```

### 2. Create virtual environment

```powershell
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
```

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
# Copy the example environment file
copy .env.example .env  # Windows
# OR
cp .env.example .env    # Linux/Mac

# Edit .env with your settings
notepad .env  # Windows
# OR
nano .env     # Linux/Mac
```

Required environment variables:
- `SMTP_HOST`: Your SMTP server (e.g., smtp.gmail.com)
- `SMTP_PORT`: SMTP port (typically 587 for TLS)
- `SMTP_USER`: Your email address
- `SMTP_PASSWORD`: Email password or app-specific password
- `SCREENSHOT_DIR`: Directory for storing screenshots (default: `Data/screenshots`)

### 5. Run the application

```bash
python main.py
```

## Configuration

### Email Service

The email service supports:
- ✅ TLS/STARTTLS encryption
- ✅ Configurable timeouts
- ✅ Detailed error logging
- ✅ Boolean return values for success/failure
- ✅ Optional exception re-raising via `raise_on_error` flag
- ✅ **HTML email support** with plain text fallback
- ✅ **File attachments** (screenshots, logs, reports)
- ✅ **Multiple recipients** (To, CC, BCC)
- ✅ **Type hints** for better IDE support

Example usage:
```python
from services.email_service import send_email

# Simple email
success = send_email(
    to_address="recipient@example.com",
    subject="Alert",
    body="System event detected"
)

# Advanced: HTML + attachments + multiple recipients
success = send_email(
    to_address=["user1@example.com", "user2@example.com"],
    subject="System Report",
    body="Plain text version",
    html_body="<h1>HTML version</h1>",
    attachments=["report.pdf", "screenshot.png"],
    cc="manager@example.com",
    bcc="archive@example.com",
    raise_on_error=False
)
```

See `examples/email_examples.py` for more usage patterns.

### Screenshot Service

Screenshots are automatically organized:
```
Data/screenshots/
└── HOSTNAME/
    └── 2025-11-20/
        ├── screenshot_20251120_143052_1.png
        ├── screenshot_20251120_143052_2.png
        └── ...
```

Features:
- Multi-monitor support
- Hostname-based organization (sanitized for filesystem safety)
- Date-based folder structure
- Automatic directory creation

## Dependencies

- `python-dotenv` - Environment variable management
- `mss` - Fast cross-platform screenshot capture

## Logging

Logs are written to:
- Console (stdout)
- `logs/system_monitor.log`

Log format:
```
2025-11-20 14:30:52,123 - services.email_service - INFO - Email sent to user@example.com
```

## Development

### Adding New Features

1. Create new service modules in `services/`
2. Add utilities to `utils/`
3. Update `config/settings.py` for new environment variables
4. Update `.env.example` with documentation

### Error Handling Best Practices

All service functions should:
- Use try/except blocks for external operations
- Log exceptions with `logger.exception()`
- Return clear success/failure indicators
- Optionally support `raise_on_error` flag for caller control

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes with clear commit messages
4. Submit a pull request

## Support

For issues or questions, please open an issue on GitHub.

---

**Author**: msicse  
**Repository**: [github.com/msicse/system_monitor](https://github.com/msicse/system_monitor)
