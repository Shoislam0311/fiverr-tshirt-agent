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
logger = logging.getLogger('final_fixed_agent')

class FinalFixedAutonomousTShirtAgent:
    def __init__(self):
        """Initialize the agent with proper API configuration"""
        self._validate_environment_vars()
        self._configure_openrouter_client()
        self._initialize_search_engines()
        logger.info("✅ Final fixed autonomous agent initialized - no syntax errors")

    def _validate_environment_vars(self):
        """Validate all required environment variables"""
        required_vars = ['TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID', 'OPENROUTER_API_KEY']
        missing_vars = []
        
        for var in required_vars:
            value = os.getenv(var)
            if not value or not value.strip():
                missing_vars.append(var)
        
        if missing_vars:
            logger.error(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
            raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")
        
        # Clean and store the variables
        self.telegram_token = self._clean_str(os.getenv('TELEGRAM_BOT_TOKEN'))
        self.chat_id = self._clean_str(os.getenv('TELEGRAM_CHAT_ID'))
        self.openrouter_key = self._clean_str(os.getenv('OPENROUTER_API_KEY'))
    
    def _clean_str(self, s: str) -> str:
        """Clean string from special characters and whitespace"""
        if not s:
            return ""
        return s.strip().replace('"', '').replace("'", '').replace(' ', '')

    def _configure_openrouter_client(self):
        """Configure the OpenRouter API client properly"""
        try:
            # Use clean httpx client without proxy conflicts
            http_client = httpx.Client(
                timeout=45.0,
                follow_redirects=True
            )
            
            # Correct OpenRouter API endpoint
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.openrouter_key,
                http_client=http_client
            )
            logger.info("✅ OpenRouter API client configured successfully")
        except Exception as e:
            logger.error(f"❌ Failed to configure OpenRouter client: {str(e)}")
            raise

    def _initialize_search_engines(self):
        """Initialize search engine configurations"""
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
        ]
        self.search_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        logger.info("✅ Search engine configurations initialized")

    def conduct_comprehensive_research(self) -> Dict[str, Any]:
        """Perform comprehensive web research across multiple platforms"""
        logger.info("🔍 Starting comprehensive market research...")
        start_time = time.time()
        
        # Initialize research results with empty data
        research_results = {
            'platforms': {},
            'research_time': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'data_points': 0
        }
        
        # Research each platform
        platforms = ['tiktok', 'instagram', 'reddit', 'pinterest', 'fiverr']
        
        for platform in platforms:
            logger.info(f"📊 Researching {platform.upper()} trends...")
            try:
                # Dynamically call the research method for each platform
                research_method = getattr(self, f'_research_{platform}_trends')
                platform_data = research_method()
                
                research_results['platforms'][platform] = platform_data
                research_results['data_points'] += len(platform_data) if isinstance(platform_data, list) else 0
                
            except AttributeError:
                logger.error(f"❌ Research method for {platform} not found")
            except Exception as e:
                logger.warning(f"⚠️ {platform} research failed: {str(e)}")
                # Add empty data for failed platform
                research_results['platforms'][platform] = []
        
        duration = time.time() - start_time
        logger.info(f"✅ Research completed in {duration:.1f} seconds with {research_results['data_points']} data points")
        return research_results

    def _research_tiktok_trends(self) -> List[Dict[str, str]]:
        """Research trending t-shirt designs on TikTok using live data"""
        logger.info("📱 Researching TikTok trends...")
        trends = []
        
        try:
            # Search TikTok via Bing since direct API access is limited
            query = "viral tshirt designs tiktok trending 2025"
            results = self._bing_search(query, max_results=5)
            
            for result in results:
                # Extract actual trend data from search results
                title = result['title']
                snippet = result['snippet']
                
                # Only add results that contain actual t-shirt design information
                if any(keyword in title.lower() or keyword in snippet.lower() 
                       for keyword in ['t-shirt', 'tee', 'shirt', 'design', 'graphic', 'print']):
                    trends.append({
                        'title': title,
                        'snippet': snippet,
                        'platform': 'tiktok',
                        'source_url': result.get('url', 'https://bing.com')
                    })
            
            if trends:
                logger.info(f"✅ Found {len(trends)} TikTok trends from live data")
                return trends
            
        except Exception as e:
            logger.warning(f"⚠️ TikTok research failed: {str(e)}")
        
        # Return empty list if research fails - no hardcoded fallbacks
        return []

    def _research_instagram_trends(self) -> List[Dict[str, str]]:
        """Research trending t-shirt designs on Instagram using live data"""
        logger.info("📸 Researching Instagram trends...")
        trends = []
        
        try:
            query = "instagram viral tshirt designs aesthetic 2025"
            results = self._bing_search(query, max_results=5)
            
            for result in results:
                title = result['title']
                snippet = result['snippet']
                
                if any(keyword in title.lower() or keyword in snippet.lower() 
                       for keyword in ['t-shirt', 'tee', 'shirt', 'design', 'aesthetic', 'trend']):
                    trends.append({
                        'title': title,
                        'snippet': snippet,
                        'platform': 'instagram',
                        'source_url': result.get('url', 'https://bing.com')
                    })
            
            if trends:
                logger.info(f"✅ Found {len(trends)} Instagram trends from live data")
                return trends
            
        except Exception as e:
            logger.warning(f"⚠️ Instagram research failed: {str(e)}")
        
        # Return empty list if research fails - no hardcoded fallbacks
        return []

    def _research_reddit_trends(self) -> List[Dict[str, str]]:
        """Research trending t-shirt designs on Reddit using live data"""
        logger.info("🤖 Researching Reddit trends...")
        trends = []
        
        try:
            query = "site:reddit.com/r/tshirtdesign trending viral designs"
            results = self._bing_search(query, max_results=5)
            
            for result in results:
                title = result['title']
                snippet = result['snippet']
                
                if any(keyword in title.lower() or keyword in snippet.lower() 
                       for keyword in ['design', 'tshirt', 'shirt', 'tee', 'thread', 'post']):
                    trends.append({
                        'title': title,
                        'snippet': snippet,
                        'platform': 'reddit',
                        'source_url': result.get('url', 'https://bing.com')
                    })
            
            if trends:
                logger.info(f"✅ Found {len(trends)} Reddit trends from live data")
                return trends
            
        except Exception as e:
            logger.warning(f"⚠️ Reddit research failed: {str(e)}")
        
        # Return empty list if research fails - no hardcoded fallbacks
        return []

    def _research_pinterest_trends(self) -> List[Dict[str, str]]:
        """Research trending t-shirt designs on Pinterest using live data"""
        logger.info("📌 Researching Pinterest trends...")
        trends = []
        
        try:
            query = "pinterest tshirt design trends 2025 minimalist aesthetic"
            results = self._bing_search(query, max_results=5)
            
            for result in results:
                title = result['title']
                snippet = result['snippet']
                
                if any(keyword in title.lower() or keyword in snippet.lower() 
                       for keyword in ['design', 'tshirt', 'shirt', 'aesthetic', 'trend', 'pin']):
                    trends.append({
                        'title': title,
                        'snippet': snippet,
                        'platform': 'pinterest',
                        'source_url': result.get('url', 'https://bing.com')
                    })
            
            if trends:
                logger.info(f"✅ Found {len(trends)} Pinterest trends from live data")
                return trends
            
        except Exception as e:
            logger.warning(f"⚠️ Pinterest research failed: {str(e)}")
        
        # Return empty list if research fails - no hardcoded fallbacks
        return []

    def _research_fiverr_trends(self) -> List[Dict[str, str]]:
        """Research trending t-shirt designs on Fiverr using live data"""
        logger.info("💼 Researching Fiverr marketplace trends...")
        trends = []
        
        try:
            query = "best selling tshirt designs fiverr 2025"
            results = self._bing_search(query, max_results=5)
            
            for result in results:
                title = result['title']
                snippet = result['snippet']
                
                if any(keyword in title.lower() or keyword in snippet.lower() 
                       for keyword in ['fiverr', 'tshirt', 'shirt', 'design', 'gig', 'best selling']):
                    trends.append({
                        'title': title,
                        'snippet': snippet,
                        'platform': 'fiverr',
                        'source_url': result.get('url', 'https://bing.com')
                    })
            
            if trends:
                logger.info(f"✅ Found {len(trends)} Fiverr trends from live data")
                return trends
            
        except Exception as e:
            logger.warning(f"⚠️ Fiverr research failed: {str(e)}")
        
        # Return empty list if research fails - no hardcoded fallbacks
        return []

    def _bing_search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """Perform Bing search and extract relevant results"""
        headers = self.search_headers.copy()
        headers['User-Agent'] = random.choice(self.user_agents)
        
        params = {
            'q': query,
            'count': max_results
        }
        
        try:
            url = "https://www.bing.com/search"
            response = requests.get(url, params=params, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            # Extract search results - Bing uses different HTML structures
            for result in soup.find_all('li', class_='b_algo'):
                title_elem = result.find('h2')
                snippet_elem = result.find('div', class_='b_caption')
                
                if title_elem and snippet_elem:
                    title = title_elem.get_text(strip=True)
                    snippet = snippet_elem.get_text(strip=True)
                    
                    if title and snippet:
                        results.append({
                            'title': title,
                            'snippet': snippet,
                            'url': result.find('a')['href'] if result.find('a') else 'https://bing.com'
                        })
            
            # Limit results
            results = results[:max_results]
            logger.info(f"✅ Bing search returned {len(results)} results for query: '{query}'")
            return results
            
        except Exception as e:
            logger.warning(f"⚠️ Bing search failed for query '{query}': {str(e)}")
            return []

    def generate_prompts_from_research(self, research_ Dict[str, Any]) -> List[str]:
        """Generate unique prompts based SOLELY on actual research data - no predefined themes"""
        logger.info("🤖 Activating MiniMax M2 agentic workflow for prompt generation...")
        
        try:
            # Extract ALL raw trend data from research - no filtering or selection
            all_research_data = []
            for platform, trends in research_data['platforms'].items():
                if isinstance(trends, list):
                    for trend in trends:
                        # Extract title and snippet from each trend
                        title = trend.get('title', '')
                        snippet = trend.get('snippet', '')
                        
                        # Combine title and snippet for comprehensive research data
                        if title and snippet:
                            all_research_data.append(f"PLATFORM: {platform.upper()}\nTITLE: {title}\nSNIPPET: {snippet}")
                        elif title:
                            all_research_data.append(f"PLATFORM: {platform.upper()}\nTITLE: {title}")
                        elif snippet:
                            all_research_data.append(f"PLATFORM: {platform.upper()}\nSNIPPET: {snippet}")
            
            # Create comprehensive research summary for AI
            research_summary = "\n\n".join(all_research_data)
            
            if not research_summary.strip():
                logger.warning("⚠️ No research data found - cannot generate prompts")
                return []  # Return empty list if no research data
            
            # Create agentic prompt for MiniMax M2 - NO HARDCODED THEMES OR EXAMPLES
            system_prompt = f"""
            You are an autonomous AI agent with full agentic capabilities. Your task is to analyze the current market research data below and generate 5 unique, ready-to-use image generation prompts for t-shirt designs.

            CURRENT MARKET RESEARCH ({research_data['research_time']}):
            {research_summary}

            AGENT INSTRUCTIONS:
            1. Analyze the research data above to identify ACTUAL current trends from the market
            2. Create 5 COMPLETELY UNIQUE prompts based SOLELY on the REAL trends from the research data
            3. Each prompt must be ready to copy-paste directly into image generators
            4. Include specific details: style, colors, composition, background, quality specifications
            5. Optimize for commercial t-shirt printing (clean lines, scalable, print-ready)
            6. Use professional design terminology and be extremely specific
            7. DO NOT use ANY examples from your training data - use ONLY the research data provided
            8. DO NOT create any prompts based on themes that exist in programming code
            9. Format: One prompt per line, numbered 1-5, with NO additional text or explanations
            10. Make each prompt commercial-ready and printing-optimized
            11. Include vector art specifications and isolated background requirements
            12. Generate prompts that reflect the actual trends found in the research data
            13. DO NOT repeat any information from this instruction in your response

            NOW GENERATE 5 UNIQUE PROMPTS BASED SOLELY ON THE RESEARCH DATA ABOVE:
            """
            
            # Generate prompts with MiniMax M2 using only research data
            completion = self.client.chat.completions.create(
                model="minimax/minimax-m2:free",
                messages=[{"role": "user", "content": system_prompt}],
                temperature=0.85,  # High creativity
                max_tokens=800,
                timeout=45.0
            )
            
            if completion and completion.choices:
                raw_content = completion.choices[0].message.content.strip()
                logger.info("✅ MiniMax M2 generated prompts from research data")
                
                # Extract clean prompts from AI response
                prompts = self._extract_clean_prompts(raw_content)
                
                if len(prompts) >= 1:  # At least 1 valid prompt
                    return prompts[:5]
            
            # Return empty list if AI generation fails - no hardcoded fallbacks
            logger.warning("⚠️ AI prompt generation failed - no prompts generated")
            return []
            
        except Exception as e:
            logger.error(f"❌ Prompt generation failed: {str(e)}")
            return []  # Return empty list if generation fails - no hardcoded fallbacks

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
                continue
            
            # Check if line contains t-shirt design keywords and is sufficiently detailed
            if (len(line) > 50 and 
                any(keyword in line.lower() for keyword in ['design', 'shirt', 'tee', 'graphic', 'print', 'vector', 'background']) and
                any(style in line.lower() for style in ['minimalist', 'vintage', 'modern', 'geometric', 'abstract', 'typography'])):
                if self._is_valid_prompt(line):
                    prompts.append(line)
        
        # Return only prompts extracted from research data - no generated fallbacks
        return prompts[:5]  # Return maximum 5 prompts

    def _is_valid_prompt(self, prompt: str) -> bool:
        """Validate that a prompt is sufficiently detailed and relevant"""
        prompt = prompt.lower()
        required_elements = [
            ('shirt' in prompt or 'tee' in prompt or 't-shirt' in prompt),
            (len(prompt) > 40),  # Minimum length
            ('design' in prompt or 'graphic' in prompt or 'print' in prompt),
            ('background' in prompt or 'isolated' in prompt or 'vector' in prompt)
        ]
        return all(required_elements)

    def send_telegram_report(self, prompts: List[str], research_ Dict[str, Any]):
        """Send comprehensive report via Telegram"""
        logger.info("📲 Sending Telegram report...")
        
        try:
            # Create report content
            report = self._create_telegram_report(prompts, research_data)
            
            # Send to Telegram
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
            result = response.json()
            
            if result.get('ok'):
                logger.info("✅ Telegram report sent successfully")
                return True
            else:
                error_desc = result.get('description', 'Unknown error')
                logger.error(f"❌ Telegram API error: {error_desc}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to send Telegram report: {str(e)}")
            return False

    def _create_telegram_report(self, prompts: List[str], research_ Dict[str, Any]) -> str:
        """Create formatted Telegram report"""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        report = f"""
🤖 <b>FINAL FIXED AUTONOMOUS T-SHIRT PROMPT GENERATOR</b>
⏱️ {current_time}
📊 <b>RESEARCH SUMMARY</b>
• Platforms analyzed: TikTok, Instagram, Reddit, Pinterest, Fiverr
• Total data points: {research_data['data_points']}
• Research completed: {research_data['research_time']}

🎨 <b>READY-TO-USE IMAGE PROMPTS</b>
<i>Copy & paste these prompts directly into Puter.js, DALL-E 3, or any image generator:</i>

"""
        
        if prompts:
            for i, prompt in enumerate(prompts, 1):
                report += f"{i}. <code>{prompt}</code>\n\n"
        else:
            report += "<b>No prompts generated</b> - No research data found or insufficient trends identified\n\n"
        
        report += """
✅ <b>USAGE INSTRUCTIONS</b>
1. <b>Copy</b> any prompt above
2. <b>Paste</b> into your image generator (index.html Puter.js)
3. <b>Generate</b> the design (takes 15-30 seconds)
4. <b>Save</b> and upload to your Fiverr gig
5. <b>Repeat</b> for all prompts to build portfolio

🔄 <b>NEXT RESEARCH CYCLE</b>
{datetime.now() + timedelta(hours=6):%Y-%m-%d %H:%M}

⚡ <b>AGENT STATUS</b>
🟢 Operating with full autonomous capabilities
🌐 Researching real-time market trends
🤖 Generating unique prompts from live data
"""
        return report

    def run_autonomous_cycle(self):
        """Run complete autonomous cycle"""
        logger.info("🚀 Starting final fixed autonomous research and prompt generation cycle...")
        start_time = time.time()
        
        try:
            # Step 1: Conduct comprehensive research
            logger.info("🔍 Step 1: Conducting market research across multiple platforms")
            research_data = self.conduct_comprehensive_research()
            
            # Step 2: Generate prompts from research
            logger.info("🤖 Step 2: Generating unique prompts from research data using agentic workflow")
            prompts = self.generate_prompts_from_research(research_data)
            
            # Step 3: Send report
            logger.info("📲 Step 3: Sending Telegram report with prompts")
            success = self.send_telegram_report(prompts, research_data)
            
            duration = time.time() - start_time
            logger.info(f"✅ Autonomous cycle completed in {duration/60:.1f} minutes. Telegram: {'Sent' if success else 'Failed'}")
            
            if not success:
                logger.warning("⚠️ Telegram report failed - cycle still completed successfully")
            
        except Exception as e:
            duration = time.time() - start_time
            logger.exception(f"❌ Autonomous cycle failed after {duration/60:.1f} minutes: {str(e)}")
            raise

def main():
    """Main entry point"""
    try:
        logger.info("🎯 Initializing Final Fixed Autonomous T-Shirt Prompt Generator")
        agent = FinalFixedAutonomousTShirtAgent()
        agent.run_autonomous_cycle()
        logger.info("🎉 Autonomous cycle completed successfully!")
        return 0
    except Exception as e:
        logger.exception(f"💥 Critical error: {str(e)}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
