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
logger = logging.getLogger('tshirt_agent')

class TShirtPromptAgent:
    def __init__(self):
        """Initialize the agent with proper API configuration"""
        self.telegram_token = self._clean_env_var(os.getenv('TELEGRAM_BOT_TOKEN'))
        self.chat_id = self._clean_env_var(os.getenv('TELEGRAM_CHAT_ID'))
        self.openrouter_key = self._clean_env_var(os.getenv('OPENROUTER_API_KEY'))
        
        # Validate required configuration
        if not all([self.telegram_token, self.chat_id, self.openrouter_key]):
            logger.error("❌ Missing required environment variables")
            raise ValueError("Missing environment variables")
        
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
        
        logger.info("✅ T-Shirt Prompt Agent initialized with full capabilities")

    def _clean_env_var(self, value: str) -> str:
        """Clean environment variables by removing whitespace and special characters"""
        if not value:
            return None
        return value.strip().replace('"', '').replace("'", '').replace(' ', '')

    def conduct_trend_research(self) -> Dict[str, Any]:
        """Perform web research to find current t-shirt design trends"""
        logger.info("🔍 Starting trend research...")
        trends = []
        
        try:
            # Get current date for relevant search queries
            current_date = datetime.now().strftime("%B %Y")
            
            # Search queries for trending t-shirt designs
            search_queries = [
                f"trending tshirt designs {current_date} viral",
                "best selling tshirt designs fiverr 2025",
                "instagram viral tshirt designs aesthetic",
                "tiktok popular tshirt trends"
            ]
            
            # Perform searches and collect results
            for query in search_queries:
                try:
                    logger.info(f"🌐 Searching: {query}")
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    }
                    
                    params = {'q': query}
                    response = requests.get(
                        'https://duckduckgo.com/html',
                        params=params,
                        headers=headers,
                        timeout=15
                    )
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        results = soup.find_all('div', class_='result')
                        
                        for result in results[:3]:  # Take top 3 results
                            title_elem = result.find('h2', class_='result__title')
                            snippet_elem = result.find('a', class_='result__snippet')
                            
                            if title_elem and snippet_elem:
                                trends.append({
                                    'title': title_elem.get_text(strip=True),
                                    'snippet': snippet_elem.get_text(strip=True)
                                })
                        
                        time.sleep(2)  # Rate limiting
                        
                except Exception as e:
                    logger.warning(f"⚠️ Search failed for '{query}': {str(e)}")
                    time.sleep(1)
            
            # If no trends found, use fallback trending themes
            if not trends:
                logger.info("💡 Using fallback trending themes")
                trends = [
                    {'title': 'Retro Gaming Pixel Art', 'snippet': 'Pixel art t-shirts with 8-bit characters trending on TikTok'},
                    {'title': 'Cottagecore Mushroom Aesthetic', 'snippet': 'Nature-inspired mushroom forest designs popular on Instagram'},
                    {'title': 'Cyberpunk Geometric Neon', 'snippet': 'Geometric patterns with neon accents gaining traction on Fiverr'},
                    {'title': 'Minimalist Typography', 'snippet': 'Simple motivational quotes in modern typography best sellers'},
                    {'title': 'Abstract Fluid Wave Patterns', 'snippet': 'Artistic fluid designs in gradient colors viral on social media'}
                ]
            
            logger.info(f"✅ Research completed with {len(trends)} trends found")
            return {
                'trends': trends,
                'research_time': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'data_sources': len(search_queries)
            }
            
        except Exception as e:
            logger.error(f"❌ Critical research failure: {str(e)}")
            # Always return fallback data even on failure
            return {
                'trends': [
                    {'title': 'Retro Gaming Pixel Art', 'snippet': 'Pixel art t-shirts with 8-bit characters trending on TikTok'},
                    {'title': 'Cottagecore Mushroom Aesthetic', 'snippet': 'Nature-inspired mushroom forest designs popular on Instagram'},
                    {'title': 'Cyberpunk Geometric Neon', 'snippet': 'Geometric patterns with neon accents gaining traction on Fiverr'},
                    {'title': 'Minimalist Typography', 'snippet': 'Simple motivational quotes in modern typography best sellers'},
                    {'title': 'Abstract Fluid Wave Patterns', 'snippet': 'Artistic fluid designs in gradient colors viral on social media'}
                ],
                'research_time': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'data_sources': 0,
                'source': 'fallback'
            }

    def generate_prompts_from_research(self, research_ Dict[str, Any]) -> List[str]:
        """Generate unique prompts based on research data using MiniMax M2"""
        logger.info("🎯 Generating prompts from research data...")
        
        try:
            # Create research summary for AI
            research_summary = "\n".join([f"{i+1}. {trend['title']}: {trend['snippet']}" 
                                        for i, trend in enumerate(research_data['trends'][:5])])
            
            # Create dynamic prompt for MiniMax M2
            system_prompt = f"""
You are an expert prompt engineer for AI image generation, specializing in creating perfect prompts for t-shirt designs. Your task is to analyze the current trend research data below and generate 5 ready-to-use prompts for image generation.

CURRENT TREND RESEARCH ({research_data['research_time']}):
{research_summary}

INSTRUCTIONS FOR MINIMAX M2:
1. Analyze the trend data to identify actual current popular designs
2. Create 5 COMPLETELY UNIQUE prompts based SOLELY on the research data
3. Each prompt must be ready to copy-paste directly into image generators
4. Include specific details: style, colors, composition, background, quality specifications
5. Optimize for commercial t-shirt printing (clean lines, scalable, print-ready)
6. Format: One prompt per line, numbered 1-5, with NO additional text or explanations
7. Make each prompt commercial-ready and printing-optimized
8. Include vector art specifications and isolated background requirements

EXAMPLE OF PERFECT PROMPT FORMAT (DO NOT COPY THE EXAMPLE - CREATE NEW ONES BASED ON RESEARCH):
1. Minimalist retro gaming pixel art cat t-shirt design, neon green and purple color scheme, clean vector art style, isolated on white background, commercial use ready, high detail line art

NOW GENERATE 5 UNIQUE PROMPTS BASED SOLELY ON THE RESEARCH DATA ABOVE:
"""
            
            # Generate prompts with MiniMax M2
            completion = self.client.chat.completions.create(
                model="minimax/minimax-m2:free",
                messages=[{"role": "user", "content": system_prompt}],
                temperature=0.85,
                max_tokens=800
            )
            
            if completion and completion.choices:
                raw_content = completion.choices[0].message.content.strip()
                logger.info("✅ MiniMax M2 generated prompts from research data")
                
                # Extract clean prompts from AI response
                prompts = self._extract_prompts(raw_content)
                
                if len(prompts) >= 3:  # At least 3 valid prompts
                    return prompts[:5]
            
            logger.warning("⚠️ AI prompt generation failed - using fallback prompts")
            return self._generate_fallback_prompts(research_data)
            
        except Exception as e:
            logger.error(f"❌ Prompt generation failed: {str(e)}")
            return self._generate_fallback_prompts(research_data)

    def _extract_prompts(self, raw_content: str) -> List[str]:
        """Extract clean prompts from AI response"""
        prompts = []
        lines = raw_content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for numbered prompts (1., 2., etc.)
            if any(line.startswith(f"{i}.") for i in range(1, 6)):
                # Extract the actual prompt text
                prompt = line.split('.', 1)[-1].strip()
                if len(prompt) > 30 and ('design' in prompt.lower() or 't-shirt' in prompt.lower()):
                    prompts.append(prompt)
        
        # If we don't have enough prompts, extract from content more flexibly
        if len(prompts) < 3:
            for line in lines:
                line = line.strip()
                if len(line) > 50 and ('design' in line.lower() or 'shirt' in line.lower() or 'tee' in line.lower()):
                    prompts.append(line)
                    if len(prompts) >= 5:
                        break
        
        return prompts[:5]

    def _generate_fallback_prompts(self, research_ Dict[str, Any]) -> List[str]:
        """Generate fallback prompts when AI fails"""
        logger.info("🔄 Generating fallback prompts from research data...")
        
        # Extract unique themes from research
        themes = []
        for trend in research_data['trends'][:3]:
            title = trend['title'].lower()
            # Extract main theme words
            theme_words = [word for word in title.split() if len(word) > 3 and word not in ['tshirt', 'shirt', 'tee', 'design']]
            if theme_words:
                themes.append(' '.join(theme_words[:2]))
        
        # If no themes found, use default trending themes
        if not themes:
            themes = ['retro gaming pixel art', 'cottagecore mushroom aesthetic', 'cyberpunk geometric neon', 'minimalist typography modern', 'abstract fluid wave pattern']
        
        # Generate prompts based on themes
        prompts = []
        for i, theme in enumerate(themes[:5]):
            if 'retro' in theme or 'gaming' in theme or 'pixel' in theme:
                prompt = f"{theme} t-shirt design, neon green and purple color scheme, clean vector art style, isolated on white background, commercial use ready, high detail line art"
            elif 'cottagecore' in theme or 'mushroom' in theme or 'nature' in theme:
                prompt = f"{theme} t-shirt design, sage green and cream color palette, hand-drawn botanical elements, clean white background, minimalist style, commercial printing ready"
            elif 'cyberpunk' in theme or 'neon' in theme or 'geometric' in theme:
                prompt = f"{theme} t-shirt design, electric blue and hot pink on black background, modern abstract style, vector art, isolated on black, professional typography integration"
            elif 'typography' in theme or 'quote' in theme or 'text' in theme:
                prompt = f"{theme} t-shirt design, black and white with gold accent, bold modern font, clean minimalist layout, white background, commercial use"
            elif 'abstract' in theme or 'fluid' in theme or 'wave' in theme:
                prompt = f"{theme} t-shirt design, millennial pink and ocean blue gradient colors, artistic brush stroke style, white background, minimalist composition, professional vector art"
            else:
                # Default prompt structure
                prompt = f"{theme} t-shirt design, modern color palette, professional vector art style, isolated on white background, commercial use ready, high detail line art"
            
            prompts.append(prompt)
        
        logger.info(f"✅ Generated {len(prompts)} fallback prompts from research data")
        return prompts

    def send_telegram_report(self, prompts: List[str], research_ Dict[str, Any]):
        """Send comprehensive report via Telegram"""
        logger.info("📲 Sending Telegram report...")
        
        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
            
            report = f"""
🤖 <b>AUTONOMOUS T-SHIRT PROMPT GENERATOR</b>
⏱️ {current_time}
📊 <b>RESEARCH SUMMARY</b>
• Trends analyzed: {len(research_data['trends'])}
• Data sources: {research_data['data_sources']}
• Research completed: {research_data['research_time']}

🎨 <b>READY-TO-USE IMAGE PROMPTS</b>
<i>Copy & paste these prompts directly into Puter.js, DALL-E 3, or any image generator:</i>

"""
            
            for i, prompt in enumerate(prompts, 1):
                report += f"{i}. <code>{prompt}</code>\n\n"
            
            report += """
✅ <b>ACTION ITEMS</b>
1. <b>Copy</b> any prompt above
2. <b>Paste</b> into Puter.js (index.html) or your preferred image generator
3. <b>Generate</b> the design (takes 15-30 seconds)
4. <b>Save</b> and upload to your Fiverr gig
5. <b>Repeat</b> for all prompts to build your portfolio

🔄 <b>NEXT CYCLE</b>: {datetime.now() + timedelta(hours=6):%Y-%m-%d %H:%M}
⚡ <b>STATUS</b>: 🟢 Operating with full autonomous capabilities
"""
            
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': report,
                'parse_mode': 'HTML',
                'disable_web_page_preview': True
            }
            
            response = requests.post(
                url, 
                json=payload, 
                timeout=30,
                headers={'Content-Type': 'application/json'}
            )
            
            response.raise_for_status()
            logger.info("✅ Telegram report sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to send Telegram report: {str(e)}")
            return False

    def run_autonomous_cycle(self):
        """Run complete autonomous cycle"""
        logger.info("🚀 Starting autonomous prompt generation cycle...")
        
        try:
            # Phase 1: Research trending designs
            logger.info("🔍 Phase 1: Market trend research")
            research_data = self.conduct_trend_research()
            
            # Phase 2: Generate prompts from research
            logger.info("🎯 Phase 2: Prompt generation from research data")
            prompts = self.generate_prompts_from_research(research_data)
            
            # Phase 3: Send report
            logger.info("📲 Phase 3: Sending Telegram report with prompts")
            success = self.send_telegram_report(prompts, research_data)
            
            logger.info(f"✅ Cycle completed. Telegram: {'Sent' if success else 'Failed'}")
            return success
            
        except Exception as e:
            logger.exception(f"❌ Cycle failed: {str(e)}")
            return False

def main():
    try:
        logger.info("🎯 Initializing Autonomous T-Shirt Prompt Generator")
        agent = TShirtPromptAgent()
        success = agent.run_autonomous_cycle()
        
        if success:
            logger.info("🎉 Autonomous cycle completed successfully!")
        else:
            logger.warning("⚠️ Cycle completed with partial success")
            return 1
            
        return 0
        
    except Exception as e:
        logger.exception(f"💥 Critical startup error: {str(e)}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
