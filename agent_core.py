import os
import time
import json
import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
import httpx
from openai import OpenAI
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('prompt_agent')

class PromptGeneratorAgent:
    def __init__(self):
        # Clean and validate environment variables
        self.telegram_token = self._clean_env_var(os.getenv('TELEGRAM_BOT_TOKEN'))
        self.chat_id = self._clean_env_var(os.getenv('TELEGRAM_CHAT_ID'))
        self.openrouter_key = self._clean_env_var(os.getenv('OPENROUTER_API_KEY'))
        
        # Validate required configuration
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
            logger.error(f"❌ Failed to configure OpenRouter API: {str(e)}")
            raise
        
        logger.info("✅ Prompt Generator Agent initialized")

    def _clean_env_var(self, value: str) -> str:
        """Clean environment variables by removing whitespace and special characters"""
        if not value:
            return None
        return value.strip().replace('"', '').replace("'", '').replace(' ', '')

    def get_trending_themes(self) -> List[str]:
        """Return current trending t-shirt design themes"""
        # In a production system, this would scrape real-time data
        # For now, we'll use a curated list of current trends
        current_date = datetime.now().strftime("%B %Y")
        return [
            f"minimalist retro gaming pixel art {current_date}",
            f"cottagecore mushroom forest aesthetic",
            f"cyberpunk geometric neon grid pattern",
            f"motivational typography modern bold font",
            f"abstract wave pattern {current_date} trend"
        ]

    def generate_image_prompts(self) -> List[str]:
        """Generate actual prompts for image generation APIs - NOT IDEAS"""
        logger.info("🎨 Generating actual image generation prompts...")
        
        trending_themes = self.get_trending_themes()
        prompts = []
        
        for theme in trending_themes:
            # These are ACTUAL PROMPTS for image generation, not just ideas
            if "retro gaming" in theme:
                prompts.append(
                    "Minimalist retro gaming pixel art cat t-shirt design, neon green and purple color scheme, clean vector art style, isolated on white background, commercial use ready, high detail line art"
                )
            elif "cottagecore mushroom" in theme:
                prompts.append(
                    "Cottagecore mushroom forest aesthetic t-shirt design, sage green and cream color palette, hand-drawn botanical elements, clean white background, minimalist style, commercial printing ready"
                )
            elif "cyberpunk geometric" in theme:
                prompts.append(
                    "Cyberpunk geometric neon grid pattern t-shirt design, electric blue and hot pink on black background, modern abstract style, vector art, isolated on black, professional typography integration"
                )
            elif "motivational typography" in theme:
                prompts.append(
                    "Modern motivational quote typography t-shirt design, bold sans-serif font with gradient effect, black and white color scheme with gold accent, clean minimalist layout, white background, commercial use"
                )
            elif "abstract wave" in theme:
                prompts.append(
                    "Abstract fluid wave pattern t-shirt design, millennial pink and ocean blue gradient colors, artistic brush stroke style, white background, minimalist composition, professional vector art style"
                )
        
        # Generate 5 unique, ready-to-use prompts
        logger.info(f"✅ Generated {len(prompts)} ready-to-use image generation prompts")
        return prompts[:5]

    def format_telegram_report(self, prompts: List[str]) -> str:
        """Format the report with actual prompts for Telegram"""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        report = f"""
🤖 <b>T-SHIRT PROMPT GENERATOR</b>
📅 {current_time}
⚡ <b>READY-TO-USE IMAGE PROMPTS</b>

<i>Copy and paste these prompts directly into your image generator:</i>

"""
        
        for i, prompt in enumerate(prompts, 1):
            report += f"{i}. <code>{prompt}</code>\n\n"
        
        report += """
✅ <b>ACTION ITEMS</b>
1. Copy any prompt above
2. Paste into Puter.js, DALL-E 3, or your preferred image generator
3. Generate the design
4. Save and upload to your Fiverr gig
5. Repeat for all prompts to build your portfolio

🔄 <b>NEXT CYCLE</b>: {datetime.now() + timedelta(hours=6):%Y-%m-%d %H:%M}
💡 <b>SYSTEM STATUS</b>: ✅ All systems operational
"""
        return report

    def send_telegram(self, message: str) -> bool:
        """Send Telegram notification with robust error handling"""
        if not self.telegram_token or not self.chat_id:
            logger.error("❌ Missing Telegram credentials")
            return False
        
        # Validate chat ID format
        try:
            chat_id = int(self.chat_id)
        except (ValueError, TypeError):
            logger.error(f"❌ Invalid chat ID format: '{self.chat_id}'")
            return False
        
        # Clean token
        token = self.telegram_token.strip()
        
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML',
            'disable_web_page_preview': True
        }
        
        try:
            logger.info(f"📤 Sending Telegram to ID: {chat_id}")
            response = requests.post(
                url,
                json=payload,
                timeout=30,
                headers={'Content-Type': 'application/json'}
            )
            
            response.raise_for_status()
            result = response.json()
            
            if result.get('ok'):
                logger.info("✅ Telegram sent successfully")
                return True
            
            error_desc = result.get('description', 'Unknown error')
            error_code = result.get('error_code', 'Unknown')
            logger.error(f"❌ Telegram error {error_code}: {error_desc}")
            return False
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Network error: {str(e)}")
            return False
        except Exception as e:
            logger.exception(f"❌ Unexpected error: {str(e)}")
            return False

    def run_cycle(self) -> bool:
        """Run the complete prompt generation cycle"""
        logger.info("🚀 Starting prompt generation cycle...")
        
        try:
            # Generate the actual prompts
            prompts = self.generate_image_prompts()
            
            # Create and send report
            report = self.format_telegram_report(prompts)
            success = self.send_telegram(report)
            
            logger.info(f"✅ Cycle completed. Telegram: {'Sent' if success else 'Failed'}")
            return success
            
        except Exception as e:
            logger.exception(f"❌ Cycle failed: {str(e)}")
            return False

def main():
    try:
        logger.info("🎯 Initializing T-Shirt Prompt Generator Agent")
        agent = PromptGeneratorAgent()
        success = agent.run_cycle()
        
        if success:
            logger.info("🎉 Prompt generation cycle completed successfully!")
        else:
            logger.warning("⚠️ Cycle completed with partial success")
            return 1
            
        return 0
        
    except ValueError as e:
        logger.error(f"❌ Configuration error: {str(e)}")
        return 1
    except Exception as e:
        logger.exception(f"💥 Critical startup error: {str(e)}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
