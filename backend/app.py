from flask import Flask, render_template, jsonify
import os
import sys

# Add the backend directory to the Python path to allow for relative imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent_core import PromptGeneratorAgent

app = Flask(__name__,
            template_folder=os.path.abspath('../frontend'),
            static_folder=os.path.abspath('../frontend/static'))

# Memoize the agent instance to avoid re-initializing on every request
agent_instance = None

def get_agent():
    global agent_instance
    if agent_instance is None:
        try:
            agent_instance = PromptGeneratorAgent()
        except ValueError as e:
            # This will be caught and sent to the frontend
            raise e
    return agent_instance

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/run-trend-analysis', methods=['POST'])
def run_trend_analysis():
    try:
        agent = get_agent()

        # Run the core logic of the agent
        trends = agent.conduct_trend_research()
        if not trends:
            return jsonify({"error": "Could not find any trends. The search may have failed."}), 500

        analyzed_trends = agent.analyze_trend_images(trends)
        if not analyzed_trends:
            return jsonify({"error": "Failed to analyze trend images with the AI model."}), 500

        prompts = agent.generate_image_prompts(analyzed_trends)
        if not prompts:
            return jsonify({"error": "Failed to generate prompts from the analyzed trends."}), 500

        # Prepare data for the frontend, limiting to the top 3 trends
        frontend_trends = [
            {
                "title": trend.get("title", "Untitled"),
                "image_url": trend.get("image_url"),
                "analysis": trend.get("analysis", "No analysis available.")
            } for trend in analyzed_trends[:3]
        ]

        return jsonify({
            "trends": frontend_trends,
            "prompts": prompts
        })

    except ValueError as e:
        # Catches missing environment variables
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        # General error handler
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)
