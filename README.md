# 🤖 24/7 Fiverr T-Shirt Agent

A simple, reliable agent that generates ready-to-use T-shirt design prompts and sends them to your Telegram every 6 hours.

## ⚡ Quick Setup (5 minutes)

1. **Create GitHub Repository**
   - Go to github.com
   - Create new public repository named `fiverr-tshirt-agent`

2. **Add Files**
   - Click "Add file" → "Create new file"
   - Create each file with the exact names and content above:
     - `.github/workflows/agent.yml`
     - `agent_core.py`
     - `requirements.txt`
     - `index.html`
     - `README.md`

3. **Set GitHub Secrets**
   - Go to repository "Settings" → "Secrets and variables" → "Actions"
   - Click "New repository secret"
   - Add these secrets:
     - `TELEGRAM_BOT_TOKEN` = your @BotFather token
     - `TELEGRAM_CHAT_ID` = your User ID from @userinfobot
     - `OPENROUTER_API_KEY` = your OpenRouter key (get from openrouter.ai)

4. **Run Workflow**
   - Go to "Actions" tab
   - Click "24/7 Fiverr T-Shirt Agent" workflow
   - Click "Run workflow"
   - Check your Telegram for the first report!

## ✅ What You'll Get

Every 6 hours, you'll receive 5 ready-to-use prompts like:
