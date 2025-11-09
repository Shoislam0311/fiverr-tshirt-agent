import os
import time
import json
import requests
from datetime import datetime
from pytrends.request import TrendReq
import openai  # Use the standard openai package

class FiverrTShirtAgent:
    def __init__(self):
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.openrouter_key = os.getenv('OPENROUTER_API_KEY')
        
       # Configure for OpenRouter
       openai.api_base = "https://openrouter.ai/api/v1"
       openai.api_key = os.getenv('OPENROUTER_API_KEY')
       openai.organization = ""  # OpenRouter requires this field
        
        self.trends = TrendReq(hl='en-US', tz=360)
        
    # Rest of your code remains the same, but replace OpenRouter calls with openai calls
    
    def generate_gig_content(self, trends_data):
        """Generate Fiverr gig content suggestions using MiniMax M2"""
        prompt = f"""
        Act as a Fiverr gig expert. Create compelling content for a T-shirt design gig.
        Current trending themes: {', '.join(trends_data['trends'][:3])}
        Trending colors: {', '.join(trends_data['colors'][:3])}
        Design styles popular now: {', '.join(trends_data['styles'][:2])}
        
        Output format:
        🎯 GIG TITLE: [catchy title under 60 characters]
        📝 SHORT DESCRIPTION: [one sentence hook]
        📦 PACKAGE IDEAS: [3 package options with prices]
        🔍 SEO KEYWORDS: [5 relevant keywords]
        """
        
        try:
            # Use OpenAI-compatible API for OpenRouter
            completion = openai.chat.completions.create(
                model="minimax/minimax-m2:free",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"OpenRouter API failed: {e}")
            return """
            🎯 GIG TITLE: Trending minimalist t-shirt designs for your brand
            📝 SHORT DESCRIPTION: I create viral-worthy t-shirt graphics that sell
            📦 PACKAGE IDEAS: 
            • Basic ($15): 1 design concept, 2 revisions
            • Standard ($30): 3 concepts, unlimited revisions  
            • Premium ($50): 5 concepts + mockups, 24hr delivery
            🔍 SEO KEYWORDS: tshirt design, custom graphic tee, minimalist shirt design, viral tshirt, brand apparel
            """
        
        try:
            completion = self.openrouter.completion(
                model="minimax/minimax-m2:free",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"OpenRouter failed: {e}")
            return """
            🎯 GIG TITLE: Trending minimalist t-shirt designs for your brand
            📝 SHORT DESCRIPTION: I create viral-worthy t-shirt graphics that sell
            📦 PACKAGE IDEAS: 
            • Basic ($15): 1 design concept, 2 revisions
            • Standard ($30): 3 concepts, unlimited revisions  
            • Premium ($50): 5 concepts + mockups, 24hr delivery
            🔍 SEO KEYWORDS: tshirt design, custom graphic tee, minimalist shirt design, viral tshirt, brand apparel
            """
    
    def run_agent_cycle(self):
        """Main agent execution cycle"""
        report = f"🤖 <b>FIVERR T-SHIRT AGENT REPORT</b>\n📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        # Phase 1: Research trends
        report += "🔍 <b>TREND RESEARCH</b>\n"
        trends_data = self.research_trends()
        report += f"🔥 Top Trends: {', '.join(trends_data['trends'][:3])}\n"
        report += f"🎨 Trending Colors: {', '.join(trends_data['colors'][:3])}\n\n"
        
        # Phase 2: Generate gig content
        report += "📝 <b>GIG CONTENT SUGGESTIONS</b>\n"
        gig_content = self.generate_gig_content(trends_data)
        report += gig_content + "\n\n"
        
        # Phase 3: Action items for you
        report += "✅ <b>ACTION ITEMS FOR YOU</b>\n"
        report += "1. ⚡ Update your Fiverr gig using the suggestions above\n"
        report += "2. 🖼️ Generate designs using Puter.js (open index.html in browser)\n"
        report += "3. 📱 Check Telegram for client order suggestions\n"
        report += "4. 🤝 Manually accept/respond to all Fiverr orders\n\n"
        
        report += "🔄 <b>NEXT RUN</b>: In 6 hours\n"
        report += "💡 <b>REMEMBER</b>: You must manually handle all Fiverr interactions!\n\n"
        
        report += "🎨 <b>FREE IMAGE GENERATION</b>\n"
        report += "Open index.html in your browser to generate unlimited T-shirt designs using Puter.js (100% free, no API keys needed)"
        
        self.send_telegram(report)
        print("✅ Agent cycle completed successfully")

if __name__ == "__main__":
    print("🚀 Starting 24/7 Fiverr T-Shirt Agent...")
    agent = FiverrTShirtAgent()
    agent.run_agent_cycle()
    print("✨ Agent cycle finished")
