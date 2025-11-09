#!/usr/bin/env python3
"""
Fiverr Client Order Assistant
A CLI tool that helps you respond to Fiverr client orders by generating:
- Professional response messages
- Design concept suggestions  
- Follow-up questions
- Ready-to-use templates

✅ 100% Fiverr Compliant - YOU manually send all messages and handle orders
✅ FREE to use - No credit card required
✅ Works with MiniMax M2 (free on OpenRouter)
✅ Integrates with your GitHub Actions workflow

Usage:
    python client_order_assistant.py "Client request goes here"
    python client_order_assistant.py --interactive
"""

import os
import sys
import json
import argparse
import textwrap
from datetime import datetime
import requests
from openrouter import OpenRouter

# Configuration - Set these in your GitHub secrets or environment variables
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

# Design styles database for better suggestions
DESIGN_STYLES = {
    "minimalist": {
        "description": "Clean, simple designs with minimal elements and plenty of white space",
        "best_for": ["corporate brands", "modern aesthetics", "easy printing"],
        "keywords": ["clean", "simple", "elegant", "modern", "uncluttered"]
    },
    "vintage": {
        "description": "Retro-inspired designs with distressed textures and classic typography",
        "best_for": ["coffee shops", "breweries", "nostalgic themes"],
        "keywords": ["retro", "distressed", "classic", "old school", "handcrafted"]
    },
    "geometric": {
        "description": "Abstract designs using shapes, patterns, and mathematical precision",
        "best_for": ["tech companies", "creative agencies", "modern fashion"],
        "keywords": ["abstract", "pattern", "symmetric", "modern", "artistic"]
    },
    "typography": {
        "description": "Text-focused designs with creative fonts and letter arrangements",
        "best_for": ["quotes", "brand names", "slogans", "motivational content"],
        "keywords": ["font", "text", "quote", "bold", "calligraphy"]
    },
    "illustrative": {
        "description": "Hand-drawn style illustrations with detailed artwork",
        "best_for": ["characters", "storytelling", "artistic brands"],
        "keywords": ["hand drawn", "illustration", "detailed", "artistic", "custom art"]
    }
}

class ClientOrderAssistant:
    def __init__(self):
        self.openrouter = OpenRouter(api_key=OPENROUTER_API_KEY) if OPENROUTER_API_KEY else None
        self.session_history = []
        
    def send_telegram(self, message):
        """Send notification to your Telegram (optional)"""
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            return
            
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                'chat_id': TELEGRAM_CHAT_ID,
                'text': message,
                'parse_mode': 'HTML'
            }
            requests.post(url, json=payload)
        except Exception as e:
            print(f"Telegram notification failed: {e}")
    
    def analyze_client_request(self, client_request):
        """Analyze the client request to extract key requirements"""
        prompt = f"""
        Analyze this Fiverr client request for a t-shirt design and extract key information:

        Client request: "{client_request}"

        Extract and format the response as JSON with these keys:
        - "client_name": (extract if mentioned, otherwise "Client")
        - "brand_name": (extract brand/business name if mentioned)
        - "design_subject": (main subject/theme requested)
        - "colors": (specific colors mentioned)
        - "style_preferences": (style keywords mentioned)
        - "special_requirements": (any special requirements like "for gym", "for coffee shop", etc.)
        - "sentiment": ("excited", "urgent", "professional", "casual")

        Keep it concise and accurate. Only include information explicitly mentioned or strongly implied.
        """
        
        try:
            if self.openrouter:
                completion = self.openrouter.completion(
                    model="minimax/minimax-m2:free",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=300
                )
                response = completion.choices[0].message.content
                
                # Clean and parse JSON response
                response = response.strip('```json').strip('```').strip()
                return json.loads(response)
            else:
                # Fallback analysis without AI
                return {
                    "client_name": "Client",
                    "brand_name": "Brand",
                    "design_subject": "custom t-shirt design",
                    "colors": ["not specified"],
                    "style_preferences": ["professional"],
                    "special_requirements": ["commercial use"],
                    "sentiment": "professional"
                }
                
        except Exception as e:
            print(f"Analysis failed: {e}")
            return {
                "client_name": "Client", 
                "brand_name": "Brand",
                "design_subject": client_request[:50] + "...",
                "colors": ["flexible"],
                "style_preferences": ["professional"],
                "special_requirements": ["ready for printing"],
                "sentiment": "professional"
            }
    
    def generate_design_concepts(self, analysis):
        """Generate 3 professional design concepts based on client analysis"""
        prompt = f"""
        You are a professional t-shirt designer responding to a Fiverr client. Create 3 unique design concepts based on this client analysis:

        Client Analysis:
        - Brand: {analysis['brand_name']}
        - Design Subject: {analysis['design_subject']}
        - Colors: {', '.join(analysis['colors'])}
        - Style Preferences: {', '.join(analysis['style_preferences'])}
        - Special Requirements: {analysis['special_requirements']}
        - Sentiment: {analysis['sentiment']}

        For each concept, provide:
        1. A catchy concept name
        2. Detailed description (2-3 sentences)
        3. Suggested color palette (2-3 colors max)
        4. Style keywords (2-3 relevant style keywords)

        Format as numbered list:
        1. [Concept Name]
           Description: [description]
           Colors: [color1, color2, color3]
           Style: [style keywords]

        2. [Concept Name]
           Description: [description]  
           Colors: [color1, color2]
           Style: [style keywords]

        3. [Concept Name]
           Description: [description]
           Colors: [color1, color2, color3]
           Style: [style keywords]

        Keep descriptions professional but engaging. Focus on commercial viability and print readiness.
        """
        
        try:
            completion = self.openrouter.completion(
                model="minimax/minimax-m2:free",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Concept generation failed: {e}")
            return """
            1. Minimalist Brand Focus
               Description: Clean, professional design focusing on the brand name with subtle supporting elements. Perfect for business use and easy recognition.
               Colors: black, white
               Style: minimalist, professional

            2. Creative Typography
               Description: Bold typography treatment of the brand name with creative letter arrangements and modern font choices. Great for making a statement.
               Colors: navy blue, gold
               Style: typography, modern

            3. Symbolic Abstract
               Description: Abstract representation of the brand concept using geometric shapes and patterns. Artistic yet professional for versatile use.
               Colors: charcoal gray, accent color
               Style: geometric, abstract
            """
    
    def generate_professional_response(self, analysis, design_concepts):
        """Generate a professional response message the user can send to client"""
        prompt = f"""
        You are a professional Fiverr freelancer responding to a t-shirt design client. Create a warm, professional response that:

        1. Acknowledges their request positively
        2. Shows you understood their needs
        3. Presents 3 design concepts clearly
        4. Asks specific follow-up questions to narrow down preferences
        5. Sets clear next steps and timeline expectations
        6. Includes appropriate closing

        Client Analysis:
        - Client Name: {analysis['client_name']}
        - Brand: {analysis['brand_name']}
        - Key Requirements: {analysis['design_subject']}, {', '.join(analysis['colors'])} colors

        Design Concepts:
        {design_concepts}

        Response Guidelines:
        - Keep it conversational but professional
        - Use emojis sparingly (1-2 maximum) for warmth
        - Include specific questions about their preferences
        - Mention 24-48 hour delivery timeline
        - Offer 2 rounds of revisions included
        - End with clear call to action

        Format as plain text ready to copy-paste into Fiverr messages.
        """
        
        try:
            completion = self.openrouter.completion(
                model="minimax/minimizer-m2:free",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=600
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Response generation failed: {e}")
            return f"""
            Hi {analysis['client_name']}! 👋

            Thank you so much for your order! I love the concept for your {analysis['brand_name']} t-shirt design - it sounds like a fantastic project.

            Based on your request, I've created 3 unique design concepts for you:

            1. **Minimalist Brand Focus**
               Clean, professional design focusing on your brand name with subtle supporting elements. Perfect for business use and easy recognition.
               Colors: Black and white
               Style: Minimalist, professional

            2. **Creative Typography**
               Bold typography treatment of your brand name with creative letter arrangements and modern font choices. Great for making a statement.
               Colors: Navy blue and gold
               Style: Typography, modern

            3. **Symbolic Abstract**
               Abstract representation of your brand concept using geometric shapes and patterns. Artistic yet professional for versatile use.
               Colors: Charcoal gray with accent color
               Style: Geometric, abstract

            To help me create the perfect design for you, could you let me know:
            ✅ Which concept resonates most with your vision?
            ✅ Do you have specific brand colors I should prioritize?
            ✅ Will this be for personal use, business merchandise, or retail sales?

            I'll deliver your first design concepts within 24 hours of your feedback. I include 2 rounds of revisions to ensure you're 100% satisfied.

            Looking forward to bringing your vision to life!

            Best regards,
            [Your Name]
            """
    
    def generate_puter_js_prompts(self, design_concepts):
        """Generate Puter.js prompts for each design concept"""
        prompt = f"""
        Convert these 3 design concepts into perfect Puter.js prompts for image generation. Each prompt should:

        1. Be highly detailed and specific
        2. Include style guidance (minimalist, vintage, etc.)
        3. Specify color palette clearly
        4. Mention "t-shirt design" and "white background" 
        5. Be optimized for commercial use and printing
        6. Include technical terms like "vector style", "clean lines", "isolated on white"

        Design Concepts:
        {design_concepts}

        Format as JSON array with these keys for each concept:
        [
          {{
            "concept_name": "Concept 1 name",
            "puter_prompt": "Detailed prompt for Puter.js",
            "recommended_model": "dall-e-3 or gpt-image-1",
            "quality_setting": "hd or high"
          }},
          {{
            "concept_name": "Concept 2 name", 
            "puter_prompt": "Detailed prompt for Puter.js",
            "recommended_model": "dall-e-3 or gpt-image-1",
            "quality_setting": "hd or high"
          }},
          {{
            "concept_name": "Concept 3 name",
            "puter_prompt": "Detailed prompt for Puter.js", 
            "recommended_model": "dall-e-3 or gpt-image-1",
            "quality_setting": "hd or high"
          }}
        ]

        Make prompts commercial-ready and printing-friendly.
        """
        
        try:
            completion = self.openrouter.completion(
                model="minimax/minimax-m2:free",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=800
            )
            response = completion.choices[0].message.content
            response = response.strip('```json').strip('```').strip()
            return json.loads(response)
        except Exception as e:
            print(f"Prompt generation failed: {e}")
            return [
                {
                    "concept_name": "Minimalist Brand Focus",
                    "puter_prompt": "Minimalist t-shirt design featuring clean typography of brand name with subtle geometric accents, professional business style, black and white color scheme, vector art style, isolated on white background, commercial use ready",
                    "recommended_model": "dall-e-3",
                    "quality_setting": "hd"
                },
                {
                    "concept_name": "Creative Typography",
                    "puter_prompt": "Bold modern typography t-shirt design with creative letter arrangement for brand name, navy blue and gold color scheme, clean vector style, isolated on white background, commercial printing ready",
                    "recommended_model": "gpt-image-1",
                    "quality_setting": "high"
                },
                {
                    "concept_name": "Symbolic Abstract",
                    "puter_prompt": "Abstract geometric t-shirt design representing brand concept with artistic patterns, charcoal gray and accent color scheme, minimalist vector art style, isolated on white background, commercial use ready",
                    "recommended_model": "dall-e-3", 
                    "quality_setting": "hd"
                }
            ]
    
    def process_client_order(self, client_request):
        """Main function to process a client order and generate all outputs"""
        print("\n" + "="*80)
        print(f"🤖 FIVERR CLIENT ORDER ASSISTANT - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("="*80)
        
        print(f"\n📋 Client Request: \"{client_request}\"\n")
        
        # Step 1: Analyze client request
        print("🔍 Analyzing client request...")
        analysis = self.analyze_client_request(client_request)
        print(f"✅ Analysis complete: {analysis['design_subject']} for {analysis['brand_name']}")
        
        # Step 2: Generate design concepts
        print("\n🎨 Generating design concepts...")
        design_concepts = self.generate_design_concepts(analysis)
        print("✅ 3 design concepts generated")
        
        # Step 3: Generate professional response
        print("\n💬 Creating professional response...")
        professional_response = self.generate_professional_response(analysis, design_concepts)
        print("✅ Professional response created")
        
        # Step 4: Generate Puter.js prompts
        print("\n⚡ Creating Puter.js prompts for image generation...")
        puter_prompts = self.generate_puter_js_prompts(design_concepts)
        print("✅ Puter.js prompts ready")
        
        # Step 5: Create final output report
        self.create_final_report(client_request, analysis, design_concepts, 
                               professional_response, puter_prompts)
        
        # Optional: Send Telegram notification
        if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
            self.send_telegram_notification(client_request, analysis)
        
        return {
            'analysis': analysis,
            'design_concepts': design_concepts,
            'response': professional_response,
            'puter_prompts': puter_prompts
        }
    
    def create_final_report(self, client_request, analysis, design_concepts, 
                          professional_response, puter_prompts):
        """Create and display the final comprehensive report"""
        
        report = f"""
        
        🎯 CLIENT ORDER ANALYSIS
        ========================
        Client Request: "{client_request}"
        Brand: {analysis['brand_name']}
        Design Subject: {analysis['design_subject']}
        Colors: {', '.join(analysis['colors'])}
        Style Preferences: {', '.join(analysis['style_preferences'])}
        Special Requirements: {analysis['special_requirements']}
        
        🎨 DESIGN CONCEPTS
        ==================
        {design_concepts}
        
        💬 READY-TO-SEND RESPONSE
        =========================
        {professional_response}
        
        ⚡ PUTER.JS IMAGE GENERATION PROMPTS
        ====================================
        Use these prompts in your index.html file to generate actual design images:
        """
        
        print(report)
        
        # Display Puter.js prompts in a clean format
        for i, prompt_data in enumerate(puter_prompts, 1):
            print(f"\n🎨 Concept {i}: {prompt_data['concept_name']}")
            print(f"   Model: {prompt_data['recommended_model']}")
            print(f"   Quality: {prompt_data['quality_setting']}")
            print(f"   Prompt: \"{prompt_data['puter_prompt']}\"")
        
        # Add Fiverr compliance reminder
        compliance_reminder = f"""
        
        ✅ FIVERR COMPLIANCE REMINDER
        =============================
        🚨 YOU MUST MANUALLY:
        • Copy and send the response above to your client in Fiverr messages
        • Generate actual images using the Puter.js prompts in index.html
        • Review all AI-generated designs before sending to client
        • Accept the order manually in Fiverr
        • Upload final design files manually through Fiverr interface
        
        🤖 AI ONLY ASSISTS WITH:
        • Research and trend analysis
        • Design concept generation (you review final)
        • Content/template suggestions (you edit and approve)
        • Workflow automation (saves you time)
        
        📱 NEXT STEPS:
        1. Copy the professional response above
        2. Paste it into your Fiverr message to the client
        3. Open index.html in your browser
        4. Use the Puter.js prompts to generate actual design images
        5. Save your favorite designs for the client
        6. Wait for client feedback before proceeding
        
        💰 COST: ~$0.02 per image generated (you pay only when you generate)
        """
        
        print(compliance_reminder)
    
    def send_telegram_notification(self, client_request, analysis):
        """Send summary to Telegram"""
        message = f"""
        🤖 NEW CLIENT ORDER ASSISTANT
        
        Client Request: "{client_request[:50]}..."
        Brand: {analysis['brand_name']}
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        
        ✅ Ready-to-send response created
        ✅ 3 design concepts generated  
        ✅ Puter.js prompts ready
        
        Check your terminal for full details!
        """
        self.send_telegram(message)
    
    def interactive_mode(self):
        """Interactive mode for manual client order processing"""
        print("\n" + "="*80)
        print("🤖 FIVERR CLIENT ORDER ASSISTANT - INTERACTIVE MODE")
        print("="*80)
        print("Enter client requests one by one. Type 'exit' or 'quit' to end.")
        
        while True:
            print("\n" + "-"*80)
            client_request = input("\n📋 Enter client request (or 'exit' to quit): ").strip()
            
            if client_request.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Exiting interactive mode. Your assistant is ready for next time!")
                break
            
            if not client_request:
                print("❌ Please enter a valid client request.")
                continue
            
            try:
                self.process_client_order(client_request)
            except Exception as e:
                print(f"❌ Error processing order: {e}")
                print("💡 Please try again or check your API keys.")

def main():
    """Main function with command line argument parsing"""
    parser = argparse.ArgumentParser(description='Fiverr Client Order Assistant')
    parser.add_argument('request', nargs='?', help='Client request text (optional if using interactive mode)')
    parser.add_argument('--interactive', '-i', action='store_true', help='Run in interactive mode')
    parser.add_argument('--test', '-t', action='store_true', help='Run test with sample client request')
    
    args = parser.parse_args()
    
    # Initialize assistant
    assistant = ClientOrderAssistant()
    
    # Check if OpenRouter API key is set
    if not OPENROUTER_API_KEY:
        print("\n" + "="*80)
        print("⚠️  WARNING: OPENROUTER_API_KEY not set!")
        print("="*80)
        print("You need to set your OpenRouter API key to use AI features.")
        print("Get your free API key at: https://openrouter.ai")
        print("Set it as a GitHub secret or environment variable named 'OPENROUTER_API_KEY'")
        print("\n💡 You can still use Puter.js for image generation without this key.")
        
        # Ask if they want to continue
        continue_anyway = input("\nDo you want to continue anyway? (y/n): ").strip().lower()
        if continue_anyway != 'y':
            print("👋 Exiting. Set your API key and try again!")
            return
    
    # Handle different modes
    if args.interactive:
        assistant.interactive_mode()
    elif args.test:
        test_request = "I need a t-shirt design for my coffee shop called 'Morning Brew'. I want something with coffee cups and mountains, modern minimalist style."
        print(f"\n🧪 Running test with sample request:\n\"{test_request}\"\n")
        assistant.process_client_order(test_request)
    elif args.request:
        assistant.process_client_order(args.request)
    else:
        print("\n" + "="*80)
        print("🤖 FIVERR CLIENT ORDER ASSISTANT")
        print("="*80)
        print("\nUsage examples:")
        print("1. Single request: python client_order_assistant.py \"Client request text\"")
        print("2. Interactive mode: python client_order_assistant.py --interactive")
        print("3. Test mode: python client_order_assistant.py --test")
        print("\n💡 Pro Tip: Use quotes around your client request if it contains spaces!")

if __name__ == "__main__":
    main()
