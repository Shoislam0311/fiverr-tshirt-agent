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
import re
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('prompt_agent')

class PromptGeneratorAgent:
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
        
        logger.info("✅ Prompt Generator Agent initialized with full capabilities")

    def _clean_env_var(self, value: str) -> str:
        """Clean environment variables by removing whitespace and special characters"""
        if not value:
            return None
        return value.strip().replace('"', '').replace("'", '').replace(' ', '')

    def conduct_trend_research(self) -> List[Dict[str, str]]:
        """Research current t-shirt design trends from multiple sources"""
        logger.info("🔍 Starting trend research for prompt generation...")
        trends = []
        
        try:
            current_date = datetime.now().strftime("%B %Y")
            
            # Search queries for trending designs
            search_queries = [
                f"trending tshirt designs {current_date} viral",
                "best selling graphic tees fiverr 2025",
                "instagram aesthetic tshirt designs popular",
                "tiktok viral tshirt design trends"
            ]
            
            # Perform searches with rate limiting
            for i, query in enumerate(search_queries):
                try:
                    logger.info(f"🌐 Searching trends: {query}")
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
                        
                        for result in results[:3]:
                            title_elem = result.find('h2', class_='result__title')
                            snippet_elem = result.find('a', class_='result__snippet')
                            
                            if title_elem and snippet_elem:
                                title = title_elem.get_text(strip=True)
                                snippet = snippet_elem.get_text(strip=True)
                                
                                # Filter for t-shirt relevant content
                                if any(keyword in title.lower() or keyword in snippet.lower() 
                                       for keyword in ['tshirt', 'shirt', 'tee', 'design', 'graphic', 'print']):
                                    trends.append({
                                        'title': title,
                                        'snippet': snippet
                                    })
                    
                    # Rate limiting between searches
                    if i < len(search_queries) - 1:
                        time.sleep(random.uniform(2.0, 4.0))
                        
                except Exception as e:
                    logger.warning(f"⚠️ Search failed for '{query}': {str(e)}")
                    time.sleep(1)
            
            # Use fallback trends if no results found
            if not trends:
                logger.info("💡 Using fallback trending themes for prompt generation")
                trends = [
                    {'title': 'Retro Gaming Pixel Art', 'snippet': 'Pixel art t-shirts with 8-bit characters trending on TikTok'},
                    {'title': 'Cottagecore Mushroom Aesthetic', 'snippet': 'Nature-inspired mushroom forest designs popular on Instagram'},
                    {'title': 'Cyberpunk Geometric Neon', 'snippet': 'Geometric patterns with neon accents gaining traction on Fiverr'},
                    {'title': 'Minimalist Typography', 'snippet': 'Simple motivational quotes in modern typography best sellers'},
                    {'title': 'Abstract Fluid Wave Patterns', 'snippet': 'Artistic fluid designs in gradient colors viral on social media'}
                ]
            
            logger.info(f"✅ Trend research completed with {len(trends)} relevant results")
            return trends
            
        except Exception as e:
            logger.error(f"❌ Critical research failure: {str(e)}")
            # Always return fallback data
            return [
                {'title': 'Retro Gaming Pixel Art', 'snippet': 'Pixel art t-shirts with 8-bit characters trending on TikTok'},
                {'title': 'Cottagecore Mushroom Aesthetic', 'snippet': 'Nature-inspired mushroom forest designs popular on Instagram'},
                {'title': 'Cyberpunk Geometric Neon', 'snippet': 'Geometric patterns with neon accents gaining traction on Fiverr'},
                {'title': 'Minimalist Typography', 'snippet': 'Simple motivational quotes in modern typography best sellers'},
                {'title': 'Abstract Fluid Wave Patterns', 'snippet': 'Artistic fluid designs in gradient colors viral on social media'}
            ]

    def generate_image_prompts(self, trends: List[Dict[str, str]]) -> List[str]:
        """Generate ready-to-use image generation prompts from trend research"""
        logger.info("🎨 Generating ready-to-use image generation prompts...")
        
        try:
            # Create research summary for AI
            research_summary = "\n".join([f"{i+1}. {trend['title']}: {trend['snippet']}" 
                                        for i, trend in enumerate(trends[:5])])
            
            # Create prompt for MiniMax M2 to generate image prompts
            prompt = f"""
You are a professional prompt engineer specializing in creating perfect prompts for AI image generation of t-shirt designs. Your task is to analyze the current trend research data and create 5 ready-to-use, production-quality prompts for image generation APIs.

CURRENT TREND RESEARCH:
{research_summary}

INSTRUCTIONS:
1. Create 5 COMPLETELY UNIQUE prompts based SOLELY on the research data above
2. Each prompt must be ready to copy-paste directly into image generators like Puter.js, DALL-E 3, or Stable Diffusion
3. Include ALL necessary details for commercial t-shirt printing:
   - Specific style descriptions (minimalist, vintage, modern, etc.)
   - Exact color schemes and combinations
   - Composition and layout details
   - Background requirements (isolated on white is standard)
   - Quality specifications (vector art, high detail, etc.)
4. Optimize prompts for commercial use:
   - Clean lines that scale well for printing
   - Avoid complex details that won't print clearly
   - Include "commercial use ready" specification
5. Format: One prompt per line, numbered 1-5, with NO additional text or explanations
6. Make each prompt printing-ready and commercial-grade

EXAMPLE OF PERFECT PROMPT FORMAT (DO NOT COPY - CREATE NEW ONES BASED ON RESEARCH):
1. Minimalist retro gaming pixel art cat t-shirt design, neon green and purple color scheme, clean vector art style, isolated on white background, commercial use ready, high detail line art

NOW GENERATE 5 UNIQUE PROMPTS BASED SOLELY ON THE RESEARCH DATA ABOVE:
"""
            
            # Generate prompts with MiniMax M2
            completion = self.client.chat.completions.create(
                model="minimax/minimax-m2:free",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.85,
                max_tokens=1000
            )
            
            if completion and completion.choices:
                raw_content = completion.choices[0].message.content.strip()
                logger.info("✅ MiniMax M2 generated unique prompts successfully")
                
                # Extract clean prompts from AI response
                prompts = self._extract_clean_prompts(raw_content)
                
                if len(prompts) >= 3:  # At least 3 valid prompts
                    return prompts[:5]
            
            logger.warning("⚠️ AI prompt generation failed - using fallback prompt generation")
            return self._generate_fallback_prompts(trends)
            
        except Exception as e:
            logger.error(f"❌ Prompt generation failed: {str(e)}")
            return self._generate_fallback_prompts(trends)

    def _extract_clean_prompts(self, raw_content: str) -> List[str]:
        """Extract clean prompts from AI response"""
        prompts = []
        lines = raw_content.split('\n')
        
        # Pattern to identify prompts (numbers followed by periods or parentheses)
        prompt_pattern = r'^\s*(\d+)[.)]\s*(.+)$'
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Try to match numbered prompt format
            match = re.match(prompt_pattern, line)
            if match:
                prompt = match.group(2).strip()
                if self._is_valid_prompt(prompt):
                    prompts.append(prompt)
        
        # If not enough prompts found, extract from content more flexibly
        if len(prompts) < 3:
            for line in lines:
                line = line.strip()
                if len(line) > 50 and ('design' in line.lower() or 'shirt' in line.lower() or 'tee' in line.lower()) and ('vector' in line.lower() or 'isolated' in line.lower() or 'background' in line.lower()):
                    if self._is_valid_prompt(line):
                        prompts.append(line)
                        if len(prompts) >= 5:
                            break
        
        return prompts[:5]  # Return maximum 5 prompts

    def _is_valid_prompt(self, prompt: str) -> bool:
        """Validate that a prompt is sufficiently detailed and relevant for t-shirt designs"""
        prompt = prompt.lower()
        required_elements = [
            ('shirt' in prompt or 'tee' in prompt or 't-shirt' in prompt),
            (len(prompt) > 40),  # Minimum length
            ('design' in prompt or 'graphic' in prompt or 'print' in prompt),
            ('background' in prompt or 'isolated' in prompt or 'vector' in prompt)
        ]
        return all(required_elements)

    def _generate_fallback_prompts(self, trends: List[Dict[str, str]]) -> List[str]:
        """Generate fallback prompts when AI fails"""
        logger.info("🔄 Generating fallback prompts from trend data...")
        
        # Extract unique themes from trends
        themes = []
        for trend in trends[:5]:
            title = trend['title'].lower()
            # Extract main theme words
            theme_words = [word for word in title.split() if len(word) > 3 and word not in ['tshirt', 'shirt', 'tee', 'design']]
            if theme_words:
                themes.append(' '.join(theme_words[:2]))
        
        # Ensure we have at least 5 themes
        default_themes = ['retro gaming pixel art', 'cottagecore mushroom aesthetic', 'cyberpunk geometric neon', 'minimalist typography modern', 'abstract fluid wave pattern']
        while len(themes) < 5:
            themes.append(default_themes[len(themes) % len(default_themes)])
        
        # Generate prompts based on themes
        prompts = []
        colors = [
            'neon green and purple color scheme',
            'sage green and cream color palette',
            'electric blue and hot pink on black background',
            'black and white with gold accent',
            'millennial pink and ocean blue gradient colors'
        ]
        styles = [
            'minimalist pixel art style',
            'hand-drawn botanical elements',
            'modern geometric style',
            'bold modern typography',
            'artistic fluid pattern'
        ]
        
        for i, theme in enumerate(themes[:5]):
            prompt = f"{theme} t-shirt design, {colors[i]}, {styles[i]}, isolated on white background, commercial use ready, high detail line art, printing optimized vector graphics"
            prompts.append(prompt)
        
        logger.info(f"✅ Generated {len(prompts)} fallback prompts from trend data")
        return prompts

    def send_telegram_report(self, prompts: List[str], trends: List[Dict[str, str]]):
        """Send comprehensive report with ready-to-use prompts via Telegram"""
        logger.info("📲 Sending Telegram report with prompts...")
        
        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
            
            report = f"""
🤖 <b>AUTONOMOUS T-SHIRT PROMPT GENERATOR</b>
⏱️ {current_time}
📊 <b>RESEARCH SUMMARY</b>
• Trends analyzed: {len(trends)}
• Research completed: {datetime.now().strftime('%Y-%m-%d %H:%M')}

🎨 <b>READY-TO-USE IMAGE PROMPTS</b>
<i>Copy & paste these prompts directly into Puter.js (index.html), DALL-E 3, or any image generator:</i>

"""
            
            for i, prompt in enumerate(prompts, 1):
                report += f"{i}. <code>{prompt}</code>\n\n"
            
            report += """
✅ <b>USAGE INSTRUCTIONS</b>
1. <b>Copy</b> any prompt above
2. <b>Paste</b> into Puter.js (index.html) or your preferred image generator
3. <b>Generate</b> the design (takes 15-30 seconds)
4. <b>Save</b> the image and upload to your Fiverr gig
5. <b>Repeat</b> for all prompts to build your portfolio

🔄 <b>NEXT RESEARCH CYCLE</b>: {datetime.now() + timedelta(hours=6):%Y-%m-%d %H:%M}
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
        """Run complete autonomous cycle to generate prompts"""
        logger.info("🚀 Starting autonomous prompt generation cycle...")
        start_time = datetime.now()
        
        try:
            # Phase 1: Research trending designs
            logger.info("🔍 Phase 1: Market trend research")
            trends = self.conduct_trend_research()
            
            # Phase 2: Generate prompts from research
            logger.info("🎯 Phase 2: Prompt generation from trend data")
            prompts = self.generate_image_prompts(trends)
            
            # Phase 3: Send report
            logger.info("📲 Phase 3: Sending Telegram report with prompts")
            success = self.send_telegram_report(prompts, trends)
            
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"✅ Cycle completed in {duration/60:.1f} minutes. Telegram: {'Sent' if success else 'Failed'}")
            return success
            
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            logger.exception(f"❌ Cycle failed after {duration/60:.1f} minutes: {str(e)}")
            return False

def main():
    try:
        logger.info("🎯 Initializing Autonomous T-Shirt Prompt Generator")
        agent = PromptGeneratorAgent()
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
