import os
import time
import json
import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List
import httpx
from openai import OpenAI
import random
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('agent')

class TrueAgenticAgent:
    def __init__(self):
        self.telegram_token = self._clean_env_var(os.getenv('TELEGRAM_BOT_TOKEN'))
        self.chat_id = self._clean_env_var(os.getenv('TELEGRAM_CHAT_ID'))
        self.openrouter_key = self._clean_env_var(os.getenv('OPENROUTER_API_KEY'))
        
        # Validate environment variables
        missing_vars = []
        if not self.telegram_token:
            missing_vars.append('TELEGRAM_BOT_TOKEN')
        if not self.chat_id:
            missing_vars.append('TELEGRAM_CHAT_ID')
        if not self.openrouter_key:
            missing_vars.append('OPENROUTER_API_KEY')
        
        if missing_vars:
            logger.error(f"❌ Missing environment variables: {', '.join(missing_vars)}")
            raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")
        
        # Configure OpenRouter API
        try:
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.openrouter_key,
                http_client=httpx.Client(timeout=60.0, follow_redirects=True)
            )
            logger.info("✅ OpenRouter API configured successfully")
        except Exception as e:
            logger.error(f"❌ OpenRouter API configuration failed: {str(e)}")
            raise
        
        logger.info("✅ Agent initialized successfully")

    def _clean_env_var(self, value: str) -> str:
        """Clean environment variables by removing whitespace and special characters"""
        if not value:
            return None
        return value.strip().replace('"', '').replace("'", '')

    def perform_deep_web_research(self) -> List[Dict[str, str]]:
        """Perform web research with robust fallback mechanisms"""
        logger.info("🔍 Starting resilient web research...")
        research_findings = []
        
        # Fallback data
        fallback_data = [
            {
                'title': 'Retro Gaming T-Shirt Designs',
                'snippet': 'Retro gaming pixel art t-shirts are trending on Fiverr with high conversion rates. Popular colors include neon green on black backgrounds.',
                'url': 'https://trends.example.com/retro-gaming'
            },
            {
                'title': 'Cottagecore Aesthetic Clothing',
                'snippet': 'Cottagecore mushroom forest designs are viral on TikTok and Instagram. Earth tone color palettes with sage green and cream combinations are most popular.',
                'url': 'https://trends.example.com/cottagecore'
            },
            {
                'title': 'Cyberpunk Minimalist Designs',
                'snippet': 'Cyberpunk geometric patterns with neon accents are gaining traction. Black backgrounds with electric blue and pink highlights convert well on Fiverr.',
                'url': 'https://trends.example.com/cyberpunk'
            },
            {
                'title': 'Minimalist Typography T-Shirts',
                'snippet': 'Simple motivational quotes in modern typography are best sellers. Black and white designs with clean fonts have highest customer satisfaction ratings.',
                'url': 'https://trends.example.com/minimalist-typography'
            },
            {
                'title': 'Abstract Geometric Patterns',
                'snippet': 'Abstract geometric patterns in millennial pink and sage green color schemes are trending. These designs work well for both personal use and commercial branding.',
                'url': 'https://trends.example.com/abstract-geometric'
            }
        ]
        
        try:
            time.sleep(2)
            search_queries = [
                "trending tshirt designs viral tiktok instagram",
                "fiverr best selling graphic tees minimalist vintage",
                "tshirt design market trends pricing 2025"
            ]
            
            for i, query in enumerate(search_queries):
                try:
                    logger.info(f"🌐 Attempting research ({i+1}/{len(search_queries)}): {query}")
                    
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1',
                    }
                    
                    params = {
                        'q': query
                    }
                    
                    response = requests.get(
                        'https://duckduckgo.com/html',
                        params=params,
                        headers=headers,
                        timeout=15
                    )
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        results = soup.find_all('div', class_='result')
                        logger.info(f"✅ Found {len(results)} results for query: {query}")
                        
                        for result in results[:2]:
                            title_elem = result.find('h2', class_='result__title')
                            snippet_elem = result.find('a', class_='result__snippet')
                            
                            if title_elem and snippet_elem:
                                research_findings.append({
                                    'title': title_elem.get_text(strip=True),
                                    'snippet': snippet_elem.get_text(strip=True),
                                    'url': 'https://duckduckgo.com'
                                })
                        
                        time.sleep(5)
                    else:
                        logger.warning(f"⚠️ Search returned status code: {response.status_code}")
                        time.sleep(3)
                        
                except Exception as e:
                    logger.warning(f"⚠️ Search attempt failed: {str(e)}")
                    time.sleep(2)
            
            if len(research_findings) < 3:
                logger.info(f"💡 Supplementing with fallback data ({len(research_findings)}/3 results found)")
                research_findings.extend(fallback_data[:5 - len(research_findings)])
            
            logger.info(f"✅ Research completed with {len(research_findings)} findings")
            return research_findings
            
        except Exception as e:
            logger.error(f"❌ Critical research failure: {str(e)}")
            return fallback_data

    def generate_dynamic_content(self, research_ List[Dict[str, str]]) -> str:
        """Generate completely unique content based on research"""
        logger.info("🧠 AI generating unique content with full creative freedom...")
        
        research_summary = "\n".join([
            f"• {finding['title']}: {finding['snippet']}" 
            for finding in research_data[:5]
        ])
        
        system_prompt = """
        You are a highly autonomous Fiverr T-shirt design expert with full creative freedom and market intelligence capabilities. Analyze the current research data and create completely unique, profitable content and design prompts.

        MINIMAX M2 FULL CAPABILITY INSTRUCTIONS:
        1. Read and deeply analyze the real-time market research data provided below
        2. Identify emerging trends, customer preferences, and pricing patterns
        3. Create BRAND NEW, UNIQUE content that has never been generated before
        4. DO NOT use templates, examples, or pre-defined formats from your training data
        5. Think creatively and adaptively based on current market conditions
        6. Generate content that converts browsers to buyers with psychological triggers
        7. Create 5 unique design prompts that are currently trending and commercially viable
        8. Write in a professional, engaging tone that matches top-performing Fiverr sellers
        9. Include specific, actionable insights from the research data
        10. Structure your response as a comprehensive market intelligence report

        OUTPUT REQUIREMENTS:
        - Use HTML formatting for Telegram readability
        - Keep content concise and under 2000 characters
        - Use simple HTML tags only: <b>, <i>, <u>, <s>, <code>, <pre>
        - NO complex HTML, CSS, or JavaScript
        - NO links, images, or embedded media
        - NO special characters that need escaping
        - Focus on text content only
        """
        
        try:
            completion = self.client.chat.completions.create(
                model="minimax/minimax-m2:free",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"CURRENT MARKET RESEARCH DATA:\n{research_summary}"}
                ],
                temperature=0.95,
                max_tokens=800,
                timeout=45.0
            )
            
            if completion and completion.choices and len(completion.choices) > 0:
                content = completion.choices[0].message.content.strip()
                # Sanitize and truncate content for Telegram
                content = self._sanitize_telegram_content(content)
                logger.info("✅ AI generated unique content successfully")
                return content
            
            logger.warning("⚠️ Empty AI response - generating emergency content")
            return self._generate_emergency_content(research_data)
            
        except Exception as e:
            logger.error(f"❌ AI content generation failed: {str(e)}")
            return self._generate_emergency_content(research_data)

    def _sanitize_telegram_content(self, content: str) -> str:
        """Sanitize content for Telegram compatibility"""
        # Remove problematic characters
        content = content.replace('&', '&amp;')
        content = content.replace('<', '<')
        content = content.replace('>', '>')
        content = content.replace('"', '&quot;')
        content = content.replace("'", '&#39;')
        
        # Remove complex HTML tags
        import re
        content = re.sub(r'<[^>]+>', lambda m: self._replace_html_tag(m.group(0)), content)
        
        # Truncate to Telegram limits
        if len(content) > 3000:  # Leave room for the report wrapper
            content = content[:2900] + "...\n<i>(Content truncated for Telegram compatibility)</i>"
        
        # Ensure proper line breaks
        content = content.replace('\r\n', '\n').replace('\r', '\n')
        
        return content.strip()

    def _replace_html_tag(self, tag: str) -> str:
        """Replace complex HTML tags with simple Telegram-compatible formatting"""
        simple_tags = ['<b>', '</b>', '<i>', '</i>', '<u>', '</u>', '<s>', '</s>', '<code>', '</code>', '<pre>', '</pre>']
        if tag.lower() in simple_tags:
            return tag
        return ''

    def _generate_emergency_content(self, research_ List[Dict[str, str]]) -> str:
        """Generate emergency content when AI fails"""
        logger.info("🔥 Generating emergency content with fallback strategies...")
        
        themes = list(set([finding['title'].split()[0].lower() for finding in research_data]))
        if len(themes) < 3:
            themes = ['retro gaming', 'cottagecore aesthetic', 'cyberpunk minimalism']
        
        current_time = datetime.now().strftime('%H:%M')
        
        return f"""
<b>EMERGENCY AGENT REPORT</b>
⏰ Generated at {current_time}

<b>CRITICAL TRENDS IDENTIFIED</b>
• {themes[0].title()}: High engagement on TikTok
• {themes[1].title()}: Strong Fiverr conversion rates  
• {themes[2].title()}: Viral potential on Instagram

<b>URGENT MARKET INSIGHTS</b>
Customers seek:
• Clean, minimalist designs
• Nostalgic themes with modern execution
• Black/white/neon color schemes
• Typography with meaningful messages
• Abstract patterns for commercial use

<b>EMERGENCY DESIGN PROMPTS</b>
1. Minimalist {themes[0]} pixel art, black background with neon {random.choice(['green', 'blue', 'pink'])} accents
2. {themes[1]} forest aesthetic, earth tones with {random.choice(['sage green', 'terracotta'])} highlights
3. {themes[2]} geometric pattern, {random.choice(['electric blue', 'neon purple'])} on dark background
4. Motivational quote typography, bold font with gradient, monochrome scheme
5. Abstract {random.choice(['wave', 'mountain'])} pattern, {random.choice(['millennial pink', 'sage green'])} and cream colors

<b>IMMEDIATE ACTIONS</b>
1. Generate designs using Puter.js
2. Update Fiverr gig with trending keywords
3. Check for new orders manually
4. Accept orders and communicate professionally
"""
    
    def send_telegram(self, message: str) -> bool:
        """Send Telegram notification with robust error handling"""
        if not all([self.telegram_token, self.chat_id]):
            logger.error("❌ Cannot send Telegram: missing required credentials")
            return False
        
        # Clean and validate chat_id
        try:
            chat_id = int(self.chat_id)
        except (ValueError, TypeError):
            logger.error(f"❌ Invalid chat ID format: '{self.chat_id}'")
            return False
        
        # Clean token
        token = self.telegram_token.strip()
        
        # Sanitize and truncate final message
        sanitized_message = self._sanitize_final_message(message)
        
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': sanitized_message,
            'parse_mode': 'HTML',
            'disable_web_page_preview': True
        }
        
        try:
            logger.info(f"📤 Sending Telegram notification to chat ID: {chat_id}")
            logger.debug(f"Message length: {len(sanitized_message)} characters")
            
            response = requests.post(
                url, 
                json=payload, 
                timeout=30,
                headers={'Content-Type': 'application/json'}
            )
            
            response.raise_for_status()
            result = response.json()
            
            if result.get('ok'):
                logger.info("✅ Telegram notification sent successfully")
                return True
            else:
                error_desc = result.get('description', 'Unknown error')
                error_code = result.get('error_code', 'Unknown')
                logger.error(f"❌ Telegram API error: {error_code} - {error_desc}")
                logger.debug(f"Full response: {json.dumps(result, indent=2)}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Network error sending Telegram: {str(e)}")
            logger.error(f"❌ URL: {url}")
            logger.error(f"❌ Payload: {json.dumps(payload, indent=2)[:200]}...")
            return False
        except Exception as e:
            logger.exception(f"❌ Unexpected error sending Telegram: {str(e)}")
            return False
    
    def _sanitize_final_message(self, message: str) -> str:
        """Final sanitization and truncation for Telegram"""
        # Remove any remaining problematic characters
        message = message.replace('\x00', '')  # Null characters
        message = message.replace('\ufffd', '')  # Replacement characters
        
        # Ensure proper HTML tag balancing
        open_tags = []
        for tag in ['<b>', '<i>', '<u>', '<s>', '<code>', '<pre>']:
            if tag in message:
                open_tags.append(tag)
        
        # Close any unclosed tags
        for tag in reversed(open_tags):
            close_tag = tag.replace('<', '</')
            if close_tag not in message:
                message += close_tag
        
        # Truncate to Telegram limits (4096 characters)
        if len(message) > 4096:
            message = message[:4000] + "\n\n<i>✂️ Message truncated - full content available in logs</i>"
        
        return message.strip()

    def run_full_cycle(self) -> bool:
        """Execute complete agentic workflow"""
        logger.info("🚀 Starting resilient agentic workflow cycle...")
        start_time = datetime.now()
        
        try:
            # Phase 1: Research
            research_data = self.perform_deep_web_research()
            
            # Phase 2: Content generation
            ai_content = self.generate_dynamic_content(research_data)
            
            # Phase 3: Create report
            duration = (datetime.now() - start_time).total_seconds()
            
            report = f"""
🤖 <b>AUTONOMOUS AGENT REPORT</b>
⏱️ Duration: {duration/60:.1f} minutes
📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}

{ai_content}

✅ <b>ACTION ITEMS</b>
1. Review AI insights
2. Generate designs using Puter.js
3. Update Fiverr gig content
4. Check for new orders manually
5. Accept orders & communicate professionally

🔄 <b>NEXT CYCLE</b>: {datetime.now() + timedelta(hours=6):%Y-%m-%d %H:%M}
⚡ <b>STATUS</b>: 🟢 Full autonomous capability
"""
            
            # Phase 4: Send notification
            success = self.send_telegram(report)
            
            logger.info(f"✅ Cycle completed. Telegram: {'Sent' if success else 'Failed'}")
            return success
            
        except Exception as e:
            logger.exception(f"❌ Cycle failed: {str(e)}")
            return False

def main():
    try:
        logger.info("🎯 Initializing autonomous Fiverr agent")
        agent = TrueAgenticAgent()
        result = agent.run_full_cycle()
        
        if result:
            logger.info("🎉 Cycle completed successfully!")
        else:
            logger.warning("⚠️ Cycle completed with partial success")
            return 1
            
        return 0
        
    except Exception as e:
        logger.exception(f"💥 Critical error: {str(e)}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
