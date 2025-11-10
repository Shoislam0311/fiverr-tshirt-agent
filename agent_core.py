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
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('prompt_agent')

class TShirtPromptGenerator:
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
        
        logger.info("✅ T-Shirt Prompt Generator Agent initialized")

    def _clean_env_var(self, value: str) -> str:
        """Clean environment variables by removing whitespace and special characters"""
        if not value:
            return None
        return value.strip().replace('"', '').replace("'", '').replace(' ', '')

    def perform_trend_research(self) -> List[str]:
        """Research current trending t-shirt design ideas from multiple sources"""
        logger.info("🔍 Researching current t-shirt design trends...")
        trend_ideas = []
        
        try:
            # Get current date for trend relevance
            current_month = datetime.now().strftime("%B")
            current_year = datetime.now().strftime("%Y")
            
            # Bing search for trending designs
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }
            
            # Search queries focused on current trends
            search_queries = [
                f"trending tshirt designs {current_month} {current_year} viral",
                f"fiverr best selling tshirt designs 2025",
                f"instagram tiktok viral tshirt designs",
                f"minimalist modern tshirt designs popular",
                f"retro gaming cottagecore cyberpunk tshirt trends"
            ]
            
            for query in search_queries[:3]:  # Limit to 3 queries for efficiency
                try:
                    bing_url = f"https://www.bing.com/search?q={query}"
                    response = requests.get(bing_url, headers=headers, timeout=15)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        results = soup.find_all('li', class_='b_algo')
                        
                        for result in results[:2]:  # Take top 2 results per query
                            title_elem = result.find('h2')
                            if title_elem:
                                title_text = title_elem.get_text(strip=True).lower()
                                # Extract design themes from titles
                                if any(keyword in title_text for keyword in ['design', 'shirt', 'tee', 'graphic', 'print', 'trend']):
                                    trend_ideas.append(title_text)
                        
                        time.sleep(2)  # Rate limiting
                        
                except Exception as e:
                    logger.warning(f"⚠️ Bing search failed for '{query}': {str(e)}")
                    time.sleep(1)
            
            # If not enough trends found, use fallback trending themes
            if len(trend_ideas) < 5:
                fallback_trends = [
                    "minimalist retro gaming pixel art",
                    "cottagecore mushroom forest aesthetic", 
                    "cyberpunk geometric neon grid",
                    "motivational typography modern",
                    "abstract wave pattern fluid art"
                ]
                trend_ideas.extend(fallback_trends[:5-len(trend_ideas)])
            
            logger.info(f"✅ Found {len(trend_ideas)} trending design ideas")
            return list(dict.fromkeys(trend_ideas))[:5]  # Deduplicate and limit to 5
            
        except Exception as e:
            logger.error(f"❌ Trend research failed: {str(e)}")
            # Always return fallback trends if research fails
            return [
                "minimalist retro gaming pixel art",
                "cottagecore mushroom forest aesthetic",
                "cyberpunk geometric neon grid",
                "motivational typography modern", 
                "abstract wave pattern fluid art"
            ]
    
    def generate_image_prompts(self, trend_ideas: List[str]) -> List[str]:
        """Convert trend ideas into ready-to-use image generation prompts"""
        logger.info("🎨 Converting trends into ready-to-use image prompts...")
        
        # First, get the AI to generate professional prompts based on trends
        trend_summary = "\n".join([f"- {idea}" for idea in trend_ideas])
        
        system_prompt = """
        You are a professional prompt engineer specializing in creating perfect prompts for AI image generation of t-shirt designs. Your task is to convert raw trend ideas into ready-to-use, production-quality prompts for image generation APIs.

        PROMPT ENGINEERING INSTRUCTIONS:
        1. Take each trend idea and convert it into a detailed, ready-to-copy-paste prompt
        2. Each prompt must be self-contained and include ALL necessary details for professional results
        3. Include specific elements for t-shirt designs:
           - Style details (minimalist, vintage, modern, etc.)
           - Color schemes and combinations
           - Background requirements (isolated on white is standard)
           - Composition and layout details
           - Quality specifications (vector art, high detail, etc.)
           - Commercial use readiness
        4. Optimize prompts for commercial t-shirt printing:
           - Clean lines and solid colors work best
           - Avoid overly complex details that won't print well
           - Ensure designs are scalable and printing-ready
        5. Structure each prompt to work perfectly with Puter.js, DALL-E 3, and similar image generators
        6. NO explanations, NO additional text - ONLY the actual prompts
        7. Format: One prompt per line, numbered 1-5

        EXAMPLE OF PERFECT PROMPT:
        "Minimalist retro gaming pixel art cat t-shirt design, neon green and purple color scheme, clean vector art style, isolated on white background, commercial use ready, high detail line art"

        EXAMPLE OF BAD PROMPT:
        "A cat design with pixels" (too vague, missing critical details)

        NOW CONVERT THESE TRENDS INTO 5 PERFECT PROMPTS:
        """
        
        try:
            completion = self.client.chat.completions.create(
                model="minimax/minimax-m2:free",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": trend_summary}
                ],
                temperature=0.7,
                max_tokens=800,
                timeout=45.0
            )
            
            if completion and completion.choices:
                raw_content = completion.choices[0].message.content.strip()
                logger.info("✅ AI generated prompt concepts successfully")
                
                # Extract actual prompts from AI response
                prompts = self._extract_prompts_from_ai_response(raw_content, trend_ideas)
                return prompts
            
            logger.warning("⚠️ Empty AI response - generating fallback prompts")
            return self._generate_fallback_prompts(trend_ideas)
            
        except Exception as e:
            logger.error(f"❌ Prompt generation failed: {str(e)}")
            return self._generate_fallback_prompts(trend_ideas)
    
    def _extract_prompts_from_ai_response(self, raw_content: str, trend_ideas: List[str]) -> List[str]:
        """Extract clean prompts from AI response"""
        prompts = []
        
        # Try to parse numbered prompts first
        lines = raw_content.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for numbered prompts (1., 2., etc.)
            if any(line.startswith(f"{i}.") for i in range(1, 6)) or any(line.startswith(f"{i})") for i in range(1, 6)):
                # Extract the actual prompt text
                prompt = line.split('.', 1)[-1].split(')', 1)[-1].strip()
                if prompt and len(prompt) > 20:  # Ensure it's substantial
                    prompts.append(prompt)
        
        # If we didn't get 5 prompts, extract from the content more flexibly
        if len(prompts) < 5:
            # Look for lines that contain t-shirt design keywords
            design_keywords = ['design', 'shirt', 'tee', 'graphic', 'print', 'vector', 'isolated', 'background']
            for line in lines:
                line = line.strip()
                if len(line) > 30 and any(keyword in line.lower() for keyword in design_keywords):
                    prompts.append(line)
                    if len(prompts) >= 5:
                        break
        
        # If still not enough, create prompts from trend ideas
        if len(prompts) < 5:
            remaining = 5 - len(prompts)
            for i in range(remaining):
                trend = trend_ideas[i % len(trend_ideas)]
                prompts.append(self._generate_prompt_from_trend(trend))
        
        return prompts[:5]
    
    def _generate_fallback_prompts(self, trend_ideas: List[str]) -> List[str]:
        """Generate fallback prompts when AI fails"""
        prompts = []
        
        for i, trend in enumerate(trend_ideas[:5]):
            prompt = self._generate_prompt_from_trend(trend)
            prompts.append(prompt)
        
        return prompts[:5]
    
    def _generate_prompt_from_trend(self, trend: str) -> str:
        """Generate a professional prompt from a single trend idea"""
        trend = trend.lower()
        
        # Color schemes based on trend
        if "retro gaming" in trend or "pixel art" in trend:
            colors = "neon green and purple color scheme"
            style = "minimalist pixel art style"
        elif "cottagecore" in trend or "mushroom" in trend or "forest" in trend:
            colors = "sage green and cream color palette"
            style = "hand-drawn botanical elements"
        elif "cyberpunk" in trend or "neon" in trend or "geometric" in trend:
            colors = "electric blue and hot pink on black background"
            style = "modern geometric style"
        elif "motivational" in trend or "typography" in trend or "quote" in trend:
            colors = "black and white with gold accent"
            style = "bold modern typography"
        elif "abstract" in trend or "wave" in trend or "fluid" in trend:
            colors = "millennial pink and ocean blue gradient"
            style = "artistic fluid pattern"
        else:
            colors = "modern color palette"
            style = "clean professional design"
        
        # Base prompt structure
        base_prompt = f"{trend} t-shirt design, {colors}, {style}, isolated on white background, commercial use ready, professional vector art"
        
        return base_prompt

    def create_telegram_report(self, prompts: List[str]) -> str:
        """Create a focused Telegram report with ready-to-use prompts"""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        report = f"""
🤖 <b>T-SHIRT PROMPT GENERATOR</b>
⏱️ {current_time}
🎯 <b>READY-TO-USE IMAGE PROMPTS</b>

<i>Copy & paste these prompts directly into Puter.js, DALL-E 3, or any image generator:</i>

"""
        
        for i, prompt in enumerate(prompts, 1):
            report += f"{i}. <code>{prompt}</code>\n\n"
        
        report += """
✅ <b>INSTRUCTIONS</b>
1. <b>Copy</b> any prompt above
2. <b>Paste</b> into Puter.js (index.html) or your preferred image generator
3. <b>Generate</b> the design (takes 15-30 seconds)
4. <b>Save</b> the image and upload to your Fiverr gig
5. <b>Repeat</b> for all 5 prompts to build your portfolio

🔄 <b>NEXT CYCLE</b>: {datetime.now() + timedelta(hours=6):%Y-%m-%d %H:%M}
⚡ <b>STATUS</b>: ✅ All prompts ready for generation
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
        logger.info("🚀 Starting T-shirt prompt generation cycle...")
        start_time = datetime.now()
        
        try:
            # Phase 1: Research trending design ideas
            logger.info("📊 Phase 1: Researching trending t-shirt designs")
            trend_ideas = self.perform_trend_research()
            logger.info(f"💡 Found trends: {', '.join(trend_ideas)}")
            
            # Phase 2: Generate ready-to-use image prompts
            logger.info("🎨 Phase 2: Generating ready-to-use image prompts")
            prompts = self.generate_image_prompts(trend_ideas)
            
            # Phase 3: Create and send Telegram report
            logger.info("📱 Phase 3: Creating prompt report")
            report = self.create_telegram_report(prompts)
            
            logger.info("📲 Phase 4: Sending prompts to Telegram")
            success = self.send_telegram(report)
            
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"✅ Cycle completed in {duration/60:.1f} minutes. Telegram: {'Sent' if success else 'Failed'}")
            return success
            
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            logger.exception(f"❌ Cycle failed after {duration/60:.1f} minutes: {str(e)}")
            
            # Send emergency notification
            emergency_report = f"""
🚨 <b>AGENT FAILURE ALERT</b>
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}
❌ Failed after {duration/60:.1f} minutes
📝 Error: {str(e)[:200]}...
🔄 Next cycle in 6 hours
"""
            try:
                self.send_telegram(emergency_report)
            except:
                logger.error("❌ Emergency notification failed")
            
            return False

def main():
    try:
        logger.info("🎯 Initializing T-Shirt Prompt Generator Agent")
        agent = TShirtPromptGenerator()
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
