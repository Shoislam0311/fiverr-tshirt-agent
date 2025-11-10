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
logger = logging.getLogger('extended_autonomous_agent')

class ExtendedAutonomousTShirtAgent:
    def __init__(self):
        """Initialize the agent with proper API configuration"""
        self._validate_environment_vars()
        self._configure_openrouter_client()
        self._initialize_search_engines()
        logger.info("✅ Extended autonomous agent initialized - will research until data found")

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

    def conduct_extended_research(self) -> Dict[str, Any]:
        """Perform extended web research until meaningful data is found"""
        logger.info("🔍 Starting extended market research - will continue until meaningful data found...")
        start_time = time.time()
        
        # Initialize research results
        research_results = {
            'platforms': {},
            'research_time': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'data_points': 0,
            'search_attempts': 0
        }
        
        # Research each platform with extended search
        platforms = ['tiktok', 'instagram', 'reddit', 'pinterest', 'fiverr']
        
        for platform in platforms:
            logger.info(f"📊 Researching {platform.upper()} trends...")
            platform_data = self._extended_platform_research(platform)
            research_results['platforms'][platform] = platform_data
            research_results['data_points'] += len(platform_data) if isinstance(platform_data, list) else 0
            research_results['search_attempts'] += 1
            
            # Add delay between platforms to avoid rate limiting
            time.sleep(2)
        
        # If no data found from primary research, expand search terms
        if research_results['data_points'] == 0:
            logger.info("⚠️ No data found from primary research - expanding search terms...")
            research_results = self._expand_search_terms(research_results)
        
        # Continue research until meaningful data is found or time limit reached
        max_research_time = 300  # 5 minutes maximum research time
        while research_results['data_points'] < 5 and (time.time() - start_time) < max_research_time:
            logger.info(f"🔍 Still searching... {research_results['data_points']} data points found so far")
            additional_data = self._additional_research()
            for platform, data in additional_data.items():
                if platform in research_results['platforms']:
                    research_results['platforms'][platform].extend(data)
                    research_results['data_points'] += len(data)
            
            if research_results['data_points'] > 0:
                logger.info(f"✅ Found {research_results['data_points']} total data points after {(time.time() - start_time):.1f} seconds")
                break
            
            time.sleep(5)  # Wait before next search attempt
        
        duration = time.time() - start_time
        logger.info(f"✅ Extended research completed in {duration:.1f} seconds with {research_results['data_points']} data points")
        return research_results

    def _extended_platform_research(self, platform: str) -> List[Dict[str, str]]:
        """Extended research for a single platform with multiple query attempts"""
        logger.info(f"🔍 Performing extended research on {platform.upper()}...")
        trends = []
        
        # Different query strategies for each platform
        base_queries = {
            'tiktok': [
                "viral tshirt designs tiktok trending 2025",
                "tiktok viral fashion trends tshirts",
                "popular tshirt designs on tiktok 2025",
                "tiktok fashion inspiration tshirts"
            ],
            'instagram': [
                "instagram viral tshirt designs aesthetic 2025",
                "instagram fashion trends tshirts",
                "popular tshirt designs on instagram 2025",
                "instagram aesthetic tshirt inspiration"
            ],
            'reddit': [
                "site:reddit.com/r/tshirtdesign trending viral designs",
                "site:reddit.com/r/FashionReps tshirt designs",
                "site:reddit.com/r/CustomShirts trending",
                "site:reddit.com/r/printful tshirt ideas"
            ],
            'pinterest': [
                "pinterest tshirt design trends 2025 minimalist aesthetic",
                "pinterest fashion inspiration tshirts",
                "popular tshirt designs on pinterest 2025",
                "pinterest tshirt graphics ideas"
            ],
            'fiverr': [
                "best selling tshirt designs fiverr 2025",
                "fiverr tshirt design gig ideas",
                "popular tshirt designs on fiverr marketplace",
                "fiverr tshirt design trends 2025"
            ]
        }
        
        queries = base_queries.get(platform, [f"{platform} tshirt design trends"])
        
        for query in queries:
            if len(trends) >= 3:  # Stop if we already have enough data
                break
                
            logger.info(f"🔍 Trying query: '{query}'")
            results = self._bing_search(query, max_results=3)
            
            for result in results:
                title = result['title']
                snippet = result['snippet']
                
                # Extract actual trend data from search results
                if any(keyword in title.lower() or keyword in snippet.lower() 
                       for keyword in ['t-shirt', 'tee', 'shirt', 'design', 'graphic', 'print', 'trend', 'viral']):
                    trends.append({
                        'title': title,
                        'snippet': snippet,
                        'platform': platform,
                        'source_url': result.get('url', 'https://bing.com')
                    })
            
            if trends:
                logger.info(f"✅ Found {len(trends)} {platform} trends")
            
            # Add delay between queries to avoid rate limiting
            time.sleep(1)
        
        return trends

    def _expand_search_terms(self, research_results: Dict[str, Any]) -> Dict[str, Any]:
        """Expand search to broader terms if primary research failed"""
        logger.info("🔍 Expanding search to broader terms...")
        
        # Broader search queries
        broad_queries = [
            "tshirt design trends 2025",
            "popular t-shirt designs 2025",
            "viral clothing designs 2025",
            "best selling tshirt designs 2025",
            "fashion tshirt design ideas 2025"
        ]
        
        for query in broad_queries:
            if research_results['data_points'] >= 5:
                break
                
            logger.info(f"🔍 Trying broad query: '{query}'")
            results = self._bing_search(query, max_results=5)
            
            for result in results:
                title = result['title']
                snippet = result['snippet']
                
                if any(keyword in title.lower() or keyword in snippet.lower() 
                       for keyword in ['t-shirt', 'tee', 'shirt', 'design', 'fashion', 'clothing', 'trend']):
                    # Add to general platform data
                    trend_data = {
                        'title': title,
                        'snippet': snippet,
                        'platform': 'general',
                        'source_url': result.get('url', 'https://bing.com')
                    }
                    
                    # Add to research results
                    if 'general' not in research_results['platforms']:
                        research_results['platforms']['general'] = []
                    research_results['platforms']['general'].append(trend_data)
                    research_results['data_points'] += 1
        
        return research_results

    def _additional_research(self) -> Dict[str, List[Dict[str, str]]]:
        """Additional research with expanded terms"""
        logger.info("🔍 Performing additional research with expanded terms...")
        
        additional_queries = [
            "current tshirt design market trends",
            "popular graphic tee designs 2025",
            "viral social media tshirt designs",
            "best tshirt design ideas for sellers",
            "tshirt design inspiration 2025"
        ]
        
        additional_data = {}
        for query in additional_queries:
            results = self._bing_search(query, max_results=3)
            platform_data = []
            
            for result in results:
                title = result['title']
                snippet = result['snippet']
                
                if any(keyword in title.lower() or keyword in snippet.lower() 
                       for keyword in ['t-shirt', 'tee', 'shirt', 'design', 'graphic', 'print']):
                    platform_data.append({
                        'title': title,
                        'snippet': snippet,
                        'platform': 'expanded',
                        'source_url': result.get('url', 'https://bing.com')
                    })
            
            if platform_data:
                additional_data['expanded'] = platform_data
                break  # Return first batch of data found
        
        return additional_data

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
        """Generate unique prompts based SOLELY on actual research data"""
        logger.info("🤖 Activating MiniMax M2 agentic workflow for prompt generation...")
        
        try:
            # Extract ALL raw trend data from research
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
            
            # Create agentic prompt for MiniMax M2
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
            
            # Return empty list if AI generation fails
            logger.warning("⚠️ AI prompt generation failed - no prompts generated")
            return []
            
        except Exception as e:
            logger.error(f"❌ Prompt generation failed: {str(e)}")
            return []  # Return empty list if generation fails

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
        
        # Return only prompts extracted from research data
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
🤖 <b>EXTENDED AUTONOMOUS T-SHIRT PROMPT GENERATOR</b>
⏱️ {current_time}
📊 <b>RESEARCH SUMMARY</b>
• Platforms analyzed: TikTok, Instagram, Reddit, Pinterest, Fiverr, General
• Total data points: {research_data['data_points']}
• Search attempts: {research_data['search_attempts']}
• Research completed: {research_data['research_time']}

🎨 <b>READY-TO-USE IMAGE PROMPTS</b>
<i>Copy & paste these prompts directly into Puter.js, DALL-E 3, or any image generator:</i>

"""
        
        if prompts:
            for i, prompt in enumerate(prompts, 1):
                report += f"{i}. <code>{prompt}</code>\n\n"
        else:
            report += "<b>No prompts generated</b> - Insufficient research data found\n\n"
        
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
🔍 Extended research until meaningful data found
"""
        return report

    def run_extended_autonomous_cycle(self):
        """Run complete extended autonomous cycle"""
        logger.info("🚀 Starting extended autonomous research and prompt generation cycle...")
        start_time = time.time()
        
        try:
            # Step 1: Conduct extended research
            logger.info("🔍 Step 1: Conducting extended market research until meaningful data found")
            research_data = self.conduct_extended_research()
            
            # Step 2: Generate prompts from research
            logger.info("🤖 Step 2: Generating unique prompts from research data using agentic workflow")
            prompts = self.generate_prompts_from_research(research_data)
            
            # Step 3: Send report
            logger.info("📲 Step 3: Sending Telegram report with prompts")
            success = self.send_telegram_report(prompts, research_data)
            
            duration = time.time() - start_time
            logger.info(f"✅ Extended autonomous cycle completed in {duration/60:.1f} minutes. Telegram: {'Sent' if success else 'Failed'}")
            
            if not success:
                logger.warning("⚠️ Telegram report failed - cycle still completed successfully")
            
        except Exception as e:
            duration = time.time() - start_time
            logger.exception(f"❌ Extended autonomous cycle failed after {duration/60:.1f} minutes: {str(e)}")
            raise

def main():
    """Main entry point"""
    try:
        logger.info("🎯 Initializing Extended Autonomous T-Shirt Prompt Generator")
        agent = ExtendedAutonomousTShirtAgent()
        agent.run_extended_autonomous_cycle()
        logger.info("🎉 Extended autonomous cycle completed successfully!")
        return 0
    except Exception as e:
        logger.exception(f"💥 Critical error: {str(e)}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
