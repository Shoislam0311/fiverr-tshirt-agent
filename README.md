# 🤖 AI T-Shirt Design Agent

A professional, AI-powered agent that conducts real-time market trend analysis and generates commercially viable t-shirt design prompts. This tool has been upgraded from a simple script to a full-fledged web application with a professional frontend and a powerful backend.

## ✨ Key Features

*   **Professional Web UI**: A sleek, modern, dark-mode interface for interacting with the agent.
*   **Keyless Trend Analysis**: Uses DuckDuckGo Search to find and analyze current t-shirt design trends without the need for an API key.
*   **Visual AI Analysis**: A multimodal AI analyzes trend images to extract insights on style, color, and composition.
*   **AI-Powered Prompt Generation**: Generates high-quality, ready-to-use prompts for AI image generators like DALL-E 3.
*   **Interactive Workflow**: A seamless, interactive experience that allows you to run the trend analysis and generate designs with the click of a button.

## 🚀 Local Setup and Execution

### 1. **Clone the Repository**

```bash
git clone https://github.com/your-username/fiverr-tshirt-agent.git
cd fiverr-tshirt-agent
```

### 2. **Set Up Environment Variables**

Create a `.env` file in the main directory and add the following keys. This is more secure and flexible than using GitHub secrets for local development.

```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
OPENROUTER_API_KEY=your_openrouter_api_key
```

*   `TELEGRAM_BOT_TOKEN`: Your token from @BotFather on Telegram.
*   `TELEGRAM_CHAT_ID`: Your user ID from @userinfobot on Telegram.
*   `OPENROUTER_API_KEY`: Your API key from [OpenRouter.ai](https://openrouter.ai).

### 3. **Install Dependencies**

Navigate to the project's root directory and install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. **Run the Backend Server**

The backend is a Flask application that serves the frontend and handles the AI logic.

```bash
python backend/app.py
```

The server will start on `http://127.0.0.1:8080`.

### 5. **Use the Web Application**

Open your web browser and navigate to `http://127.0.0.1:8080`. You can now use the professional web interface to:

*   **Analyze market trends**: Click the "Analyze Latest Trends" button to have the AI find and analyze the latest t-shirt designs.
*   **Generate design prompts**: The AI will automatically generate a list of suggested prompts based on its analysis.
*   **Create t-shirt designs**: Select a prompt, choose an AI model, and click "Generate T-Shirt Design" to create your own unique designs.

## 📁 Project Structure

The project has been restructured for better organization and scalability:

*   **`backend/`**: Contains the core Python application logic.
    *   `app.py`: The Flask web server that powers the application.
    *   `agent_core.py`: The main agent logic for trend analysis and prompt generation.
    *   `client_order_assistant.py`: A helper script for processing client orders.
*   **`frontend/`**: Contains the professional web interface.
    *   `index.html`: The main HTML file.
    *   `static/`: Contains the CSS and JavaScript files for the frontend.
        *   `style.css`: The stylesheet for the modern, dark-mode UI.
        *   `script.js`: The JavaScript for handling user interactions and API calls.
*   **`requirements.txt`**: A list of all the Python dependencies for the project.
*   **`README.md`**: This file, providing an overview of the project and setup instructions.

## 🤖 Automated Workflow

This project is configured to run automatically using GitHub Actions. The workflow, defined in `.github/workflows/agent.yml`, will execute the agent every 6 hours. This ensures that you'll receive a steady stream of fresh, trend-based design prompts delivered directly to your Telegram.

You can also trigger the workflow manually by navigating to the "Actions" tab in your GitHub repository and clicking the "Run workflow" button.
