# Twitter Crypto Sentiment Analyzer

This Django-based application connects to Twitter, monitors tweets from specific users in real-time, and performs sentiment analysis on those tweets concerning cryptocurrency tokens. The analyzed results are then broadcasted via a WebSocket to be displayed in a web interface.

## Table of Contents

1. [Features]
2. [Directory Structure]
3. [Installation]
4. [Usage]
5. [Contributing]
6. [License]

1 Features

- Real-time tweet monitoring from pre-defined Twitter users.
- Sentiment analysis using OpenAI to determine the sentiment towards cryptocurrency tokens mentioned in the tweet.
- WebSocket integration for live updates in the web interface.
- Efficient database structures for storing tweets, users, and sentiment analysis results.

2 Directory Structure

```
.
├── analyze_tweet           # Contains code for sentiment analysis.
├── callTwitter             # Handles real-time monitoring of Twitter.
├── database_manager        # ORM models and database utilities.
├── static/twitter          # Static assets for the web interface.
├── tw1tter_bot_b1nance     # Main application module.
├── twitter                 # Additional module.
├── websocketProcessor      # Handles WebSocket connections and broadcasting.
├── .env.SAMPLE             # Sample environment variables.
├── .gitignore              # Git ignore file.
├── Dockerfile              # Docker configuration file.
├── db.sqlite3              # SQLite database file.
├── docker-compose.yml      # Docker compose configuration.
└── manage.py               # Django management script.
```

## Installation

### Prerequisites

- Python 3.8+
- Docker (optional)

### Steps

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/twitter-crypto-sentiment-analyzer.git
    cd twitter-crypto-sentiment-analyzer
    ```

2. **Set up a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up Environment Variables**:
    - Rename `.env.SAMPLE` to `.env`.
    - Fill in the required environment variables like `OPENAI_API_KEY`, `TWITTER_KEY`, etc.

5. **Run Migrations**:
    ```bash
    python manage.py migrate
    ```

6. **(Optional) Using Docker**:
    ```bash
    docker-compose up --build
    ```

## Usage

1. **Start the Django Server**:
    ```bash
    python manage.py runserver
    ```

2. **Access the Web Interface**:
    - Open a browser and navigate to `http://localhost:8000/`.

3. **Monitoring Tweets**:
    - The application will automatically start monitoring tweets from the specified users in `calltwitter.py`.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---
