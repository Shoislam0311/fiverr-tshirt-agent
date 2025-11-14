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
from duckduckgo_search import DDGS

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
            raise ValueError("Missing environment variables: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, and OPENROUTER_API_KEY must be set.")

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

    def conduct_trend_research(self) -> List[Dict[str, Any]]:
        """Research current t-shirt design trends using keyless search"""
        logger.info("🔍 Starting keyless trend research...")
        trends = []

        try:
            current_date = datetime.now().strftime("%B %Y")
            search_queries = [
                f"trending t-shirt designs {current_date}",
                "best selling graphic tees on etsy",
                "pinterest popular t-shirt aesthetics",
                "top instagram t-shirt trends"
            ]

            with DDGS() as ddgs:
                for query in search_queries:
                    logger.info(f"🌐 Searching for: '{query}'")
                    results = list(ddgs.images(query, max_results=5))

                    for result in results:
                        trends.append({
                            "title": result.get("title", "Untitled"),
                            "source": result.get("url", "Unknown"),
                            "image_url": result.get("image", ""),
                            "query": query
                        })

            logger.info(f"✅ Found {len(trends)} potential trend images.")
            return trends

        except Exception as e:
            logger.error(f"❌ Trend research failed: {str(e)}")
            return []

    def analyze_trend_images(self, trends: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze images using a multimodal AI to extract design insights"""
        logger.info(f"🖼️ Analyzing {len(trends)} trend images with multimodal AI...")
        analyzed_trends = []

        for trend in trends:
            try:
                response = self.client.chat.completions.create(
                    model="google/gemini-flash-1.5",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Analyze this t-shirt design image. Describe the main subject, style (e.g., minimalist, vintage, abstract), color palette, and overall mood. Provide a concise, one-sentence summary of the design concept."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": trend["image_url"]
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=200
                )

                if response.choices:
                    analysis = response.choices[0].message.content
                    analyzed_trends.append({**trend, "analysis": analysis})
                    logger.info(f"✅ Successfully analyzed image: {trend['title']}")

            except Exception as e:
                logger.warning(f"⚠️ Failed to analyze image {trend['title']}: {str(e)}")

        logger.info(f"✅ Analysis complete. {len(analyzed_trends)} images successfully analyzed.")
        return analyzed_trends

    def generate_image_prompts(self, trends: List[Dict[str, Any]]) -> List[str]:
        """Generate ready-to-use image generation prompts from analyzed trend data"""
        logger.info("🎨 Generating professional image prompts from analyzed trends...")

        if not trends:
            logger.warning("No trends to generate prompts from. Using fallback prompts.")
            return self._generate_fallback_prompts()

        try:
            research_summary = "\n".join(
                [f"- Image from '{trend['source']}': {trend['analysis']}" for trend in trends]
            )

            prompt = f"""
You are a professional prompt engineer for AI image generators, specializing in commercially viable t-shirt designs. Analyze the following trend analysis from recent t-shirt images and generate 5 production-quality prompts.

**Trend Analysis:**
{research_summary}

**Instructions:**
1.  Create 5 unique, detailed prompts inspired by the analysis.
2.  Each prompt must be ready for a text-to-image API like DALL-E 3.
3.  Include critical details for t-shirt printing: style (e.g., minimalist vector, vintage screen-print), color palette, composition, and background (isolated on white is standard).
4.  Optimize for commercial use: clean lines, scalable details, and clear subject matter.
5.  Format: A numbered list of 5 prompts. No extra explanations.

**Example of a perfect prompt:**
*Minimalist single-line art of a cat, sleek and modern, black ink on a white background, vector style, high detail, commercial use ready.*

Now, generate 5 unique prompts based on the trend analysis:
"""

            completion = self.client.chat.completions.create(
                model="minimax/minimax-m2:free",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.9,
                max_tokens=1000
            )

            if completion and completion.choices:
                raw_content = completion.choices[0].message.content.strip()
                prompts = self._extract_clean_prompts(raw_content)
                if len(prompts) >= 3:
                    logger.info("✅ Successfully generated prompts from trend analysis.")
                    return prompts[:5]

            logger.warning("⚠️ AI prompt generation failed, using fallback prompts.")
            return self._generate_fallback_prompts()

        except Exception as e:
            logger.error(f"❌ Prompt generation failed: {str(e)}")
            return self._generate_fallback_prompts()

    def _extract_clean_prompts(self, raw_content: str) -> List[str]:
        """Extracts clean, numbered prompts from a raw text block."""
        prompts = []
        lines = raw_content.split('\n')
        prompt_pattern = r'^\s*\d+[.)]\s*(.+)$'

        for line in lines:
            match = re.match(prompt_pattern, line)
            if match:
                prompt = match.group(1).strip()
                if len(prompt) > 30: # Basic validation
                    prompts.append(prompt)
        return prompts

    def _generate_fallback_prompts(self) -> List[str]:
        """Provides a set of high-quality fallback prompts."""
        logger.info("🔄 Generating fallback prompts.")
        return [
            "Minimalist geometric wolf head, clean vector lines, black and gold color scheme, isolated on a white background, commercial printing ready.",
            "Vintage-style sunset over a mountain range, distressed texture, retro color palette (orange, yellow, brown), detailed illustration, for screen printing.",
            "Abstract cyberpunk brain with glowing neon circuits, futuristic and detailed, on a black t-shirt background, vibrant colors (pink, blue, purple).",
            "Hand-drawn botanical illustration of a monstera leaf, detailed line work, sage green and white, minimalist and elegant, vector art.",
            "Bold typography design with the word 'CREATE', letters breaking apart into geometric shapes, inspirational and modern, black and white with a single accent color."
        ]

    def send_telegram_report(self, prompts: List[str], trends: List[Dict[str, Any]]):
        """Send a comprehensive report with prompts and trend insights via Telegram."""
        logger.info("📲 Sending enhanced Telegram report...")

        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M')

            # Create a summary of the analyzed trends
            trend_summary = "\n".join(
                [f"• <b>{trend['title']}</b> (from {trend['source']}): <i>{trend.get('analysis', 'Analysis pending...')}</i>" for trend in trends[:3]]
            )

            report = f"""
🤖 <b>AI T-SHIRT DESIGN AGENT REPORT</b>
⏱️ {current_time}

📊 <b>VISUAL TREND ANALYSIS</b>
{trend_summary}

🎨 <b>READY-TO-USE IMAGE PROMPTS</b>
<i>Based on the latest visual trends. Copy and paste into the generator:</i>

"""

            for i, prompt in enumerate(prompts, 1):
                report += f"{i}. <code>{prompt}</code>\n\n"

            report += f"""
✅ <b>NEXT STEPS</b>
1.  Copy a prompt and paste it into the web UI.
2.  Generate designs and save your favorites.
3.  Upload to your Fiverr gig to attract new clients.

🔄 <b>Next research cycle will begin in 6 hours.</b>
"""

            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': report,
                'parse_mode': 'HTML',
                'disable_web_page_preview': True
            }

            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            logger.info("✅ Telegram report sent successfully.")

        except Exception as e:
            logger.error(f"❌ Failed to send Telegram report: {str(e)}")

    def run_autonomous_cycle(self):
        """Run the complete, enhanced autonomous cycle."""
        logger.info("🚀 Starting enhanced autonomous cycle...")
        start_time = time.time()

        try:
            # Phase 1: Professional trend research
            trends = self.conduct_trend_research()

            # Phase 2: AI-powered image analysis
            analyzed_trends = self.analyze_trend_images(trends)

            # Phase 3: Generate prompts from visual insights
             prompts = self.generate_image_prompts(analyzed_trends)

            # Phase 4: Send comprehensive report
            self.send_telegram_report(prompts, analyzed_trends)

            duration = time.time() - start_time
            logger.info(f"✅ Enhanced cycle completed in {duration:.2f} seconds.")

        except Exception as e:
            logger.exception(f"❌ A critical error occurred in the autonomous cycle: {str(e)}")

def main():
    try:
        logger.info("🎯 Initializing Enhanced T-Shirt Design Agent")
        agent = PromptGeneratorAgent()
        agent.run_autonomous_cycle()

    except Exception as e:
        logger.exception(f"💥 Critical startup error: {str(e)}")

if __name__ == "__main__":
    main()
