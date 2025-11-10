import os
import time
import json
import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, Any
import httpx
from openai import OpenAI
from duckduckgo_search import DDGS

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('agent')

class TrueAgenticAgent:
    def __init__(self):
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.openrouter_key = os.getenv('OPENROUTER_API_KEY')
        
        if not all([self.telegram_token, self.chat_id, self.openrouter_key]):
            logger.error("Missing required environment variables")
            raise ValueError("Missing environment variables")
        
        # Configure OpenRouter API
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.openrouter_key,
            http_client=httpx.Client(timeout=60.0, follow_redirects=True)
        )
        
        # Initialize web search
        self.ddgs = DDGS(timeout=30)
        logger.info("Agent initialized with full web search capability")

    def perform_deep_web_research(self) -> str:
        """Perform real-time web research and return raw findings"""
        logger.info("🔍 Starting deep web research...")
        research_findings = []
        
        # Dynamic search queries based on current date
        current_date = datetime.now().strftime("%B %Y")
        search_queries = [
            f"trending tshirt designs {current_date} viral",
            f"fiverr best selling graphic tees {current_date}",
            f"social media viral tshirt designs tiktok instagram",
            f"tshirt design market trends {current_date} pricing",
            f"emerging tshirt styles minimalist vintage geometric"
        ]
        
        for query in search_queries:
            try:
                logger.info(f"🌐 Researching: {query}")
                results = self.ddgs.text(query, max_results=5)
                
                for result in results:
                    research_findings.append({
                        'title': result.get('title', ''),
                        'snippet': result.get('body', ''),
                        'url': result.get('href', '')
                    })
                
                time.sleep(2)  # Rate limiting
                
            except Exception as e:
                logger.warning(f"⚠️ Search failed: {str(e)}")
        
        # Return raw research data for AI to process
        logger.info(f"✅ Research completed with {len(research_findings)} findings")
        return json.dumps(research_findings, indent=2)

    def generate_dynamic_content(self, research_data: str) -> str:
        """Generate completely unique content based on research - NO TEMPLATES"""
        logger.info("🧠 AI processing research data and generating unique content...")
        
        # Pure instructions for MiniMax M2 - no templates, no constraints
        system_prompt = """
        You are a highly autonomous Fiverr T-shirt design expert AI with full web research capabilities. Your task is to analyze real-time market research data and create completely unique, profitable Fiverr gig content and design prompts.

        INSTRUCTIONS FOR MINIMAX M2:
        1. Read and analyze the raw web research data provided
        2. Identify emerging trends, pricing patterns, and customer preferences
        3. Create BRAND NEW, UNIQUE content that has never been used before
        4. DO NOT use templates, examples, or pre-defined formats from your training
        5. Think creatively and adaptively based on current market conditions
        6. Generate content that converts browsers to buyers
        7. Create 5 unique design prompts that are currently trending
        8. Write in a professional, engaging tone that matches Fiverr's top sellers
        9. Include specific, actionable insights from the research data
        10. Structure your response as a comprehensive market report with actionable next steps

        KEY CAPABILITIES:
        - You can research the web independently
        - You can analyze market trends in real-time
        - You can create unique, profitable content
        - You can generate viral design prompts
        - You can adapt to changing market conditions
        - You have full creative freedom to innovate

        OUTPUT FORMAT:
        Use HTML formatting for Telegram readability
        Include your analysis, insights, and recommendations
        Create 5 unique design prompts based on current trends
        Provide specific action items for the human agent
        """
        
        # Let the AI create completely unique content
        completion = self.client.chat.completions.create(
            model="minimax/minimax-m2:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"WEB RESEARCH DATA:\n{research_data}"}
            ],
            temperature=0.9,
            max_tokens=1000
        )
        
        return completion.choices[0].message.content

    def send_telegram(self, message: str) -> bool:
        """Send Telegram notification"""
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'HTML',
            'disable_web_page_preview': True
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            result = response.json()
            return result.get('ok', False)
        except Exception as e:
            logger.error(f"❌ Telegram failed: {str(e)}")
            return False

    def run_full_cycle(self) -> bool:
        """Execute complete agentic workflow"""
        logger.info("🚀 Starting true agentic workflow cycle...")
        start_time = datetime.now()
        
        try:
            # Phase 1: Deep web research
            research_data = self.perform_deep_web_research()
            
            # Phase 2: AI generates unique content with full capability
            ai_content = self.generate_dynamic_content(research_data)
            
            # Phase 3: Create final report with raw AI output
            duration = (datetime.now() - start_time).total_seconds()
            final_report = f"""
🤖 <b>TRUE AGENTIC WORKFLOW REPORT</b>
⏱️ Completed in {duration/60:.1f} minutes
📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}

🔍 <b>RESEARCH SUMMARY</b>
• Performed deep web search across 5 dynamic queries
• Analyzed {research_data.count('title')} unique sources
• Extracted real-time market intelligence

🧠 <b>AI GENERATED CONTENT</b>
{ai_content}

✅ <b>ACTION ITEMS</b>
1. Review AI's unique content and insights
2. Use the generated design prompts in Puter.js
3. Update your Fiverr gig with the fresh, unique content
4. Check for new client orders
5. Manually accept/respond to all orders (required by Fiverr)

🔄 <b>NEXT CYCLE</b>: {datetime.now() + timedelta(hours=6):%Y-%m-%d %H:%M}
⚡ <b>AGENT STATUS</b>: 🟢 Operating with full autonomous capability
            """
            
            # Send the completely unique AI-generated content
            success = self.send_telegram(final_report)
            logger.info(f"✅ Cycle completed. Telegram status: {'Sent' if success else 'Failed'}")
            return success
            
        except Exception as e:
            logger.exception(f"❌ Cycle failed: {str(e)}")
            return False

def main():
    try:
        agent = TrueAgenticAgent()
        agent.run_full_cycle()
        return 0
    except Exception as e:
        logger.exception(f"💥 Critical error: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
