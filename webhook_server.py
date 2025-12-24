#!/usr/bin/env python3
"""
Minimal webhook server for ElevenLabs agent integration
Provides property search from HafH travel stories data
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random

app = Flask(__name__)
CORS(app)

# Cache for landing page HTML (built once at startup)
CACHED_INDEX_HTML = None

# Load sample properties from travel stories
PROPERTIES = []

def load_sample_data():
    """Load ALL properties from hafh_stories"""
    global PROPERTIES
    try:
        with open('data/hafh_stories.json', 'r', encoding='utf-8') as f:
            stories = json.load(f)  # Load as JSON array
            count = 0
            for story in stories:
                # Load ALL properties (removed limit)
                try:
                    prop = {
                        'name': story.get('name', 'Unknown Property'),
                        'prefecture': story.get('prefecture', ''),
                        'country': story.get('country', 'JP'),
                        'description': story.get('ts_stay_text', story.get('ts_text', '')),
                        'likes': story.get('likes_count', 0)
                    }
                    if prop['name'] and prop['name'] != 'Unknown Property':
                        PROPERTIES.append(prop)
                        count += 1
                except:
                    continue
        print(f"✅ Loaded {len(PROPERTIES)} properties")
    except Exception as e:
        print(f"⚠️  Could not load data: {e}")
        # Fallback sample data
        PROPERTIES = [
            {
                'name': 'Mountain Retreat Nagano',
                'prefecture': 'Nagano',
                'country': 'JP',
                'description': 'Peaceful mountain property with stunning views. Guests love the serene atmosphere.',
                'likes': 45
            },
            {
                'name': 'Kyoto Traditional Guesthouse',
                'prefecture': 'Kyoto',
                'country': 'JP',
                'description': 'Authentic Japanese experience in historic Kyoto. Traditional architecture and warm hospitality.',
                'likes': 38
            }
        ]

def build_index_html():
    """Build simple landing page with embedded ElevenLabs widget"""
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>KABUK AI Travel Assistant</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            :root {{
                --kabuk-pink: #E91E63;
                --kabuk-purple: #8B5CF6;
                --kabuk-dark: #1a1a1a;
                --kabuk-light: #FAF8F6;
            }}
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: system-ui, -apple-system, sans-serif;
                background: var(--kabuk-light);
                color: var(--kabuk-dark);
                min-height: 100vh;
                display: flex;
                flex-direction: column;
            }}
            .header {{
                background: var(--kabuk-dark);
                padding: 20px 40px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .logo {{
                font-size: 32px;
                font-weight: 800;
                color: var(--kabuk-pink);
                letter-spacing: 1.5px;
            }}
            .subtitle {{
                color: #999;
                font-size: 14px;
                margin-top: 5px;
            }}
            .main {{
                flex: 1;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 40px 20px;
            }}
            .widget-container {{
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.1);
                max-width: 600px;
                width: 100%;
                text-align: center;
            }}
            .widget-container h1 {{
                font-size: 32px;
                margin-bottom: 15px;
                color: var(--kabuk-dark);
            }}
            .widget-container p {{
                color: #666;
                font-size: 16px;
                margin-bottom: 30px;
                line-height: 1.6;
            }}
            .elevenlabs-widget {{
                min-height: 400px;
                background: linear-gradient(135deg, var(--kabuk-purple) 0%, #A855F7 100%);
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                padding: 40px;
                margin-bottom: 20px;
            }}
            .placeholder {{
                text-align: center;
            }}
            .placeholder h3 {{
                font-size: 20px;
                margin-bottom: 10px;
            }}
            .placeholder p {{
                opacity: 0.9;
                color: white;
                font-size: 14px;
            }}
            .details-link {{
                display: inline-block;
                color: var(--kabuk-purple);
                text-decoration: none;
                font-size: 14px;
                margin-top: 20px;
                transition: opacity 0.2s;
            }}
            .details-link:hover {{
                opacity: 0.7;
            }}
            .footer {{
                background: var(--kabuk-dark);
                color: #999;
                padding: 20px;
                text-align: center;
                font-size: 12px;
            }}
            @media (max-width: 768px) {{
                .header {{ padding: 15px 20px; }}
                .logo {{ font-size: 24px; }}
                .widget-container {{ padding: 25px; }}
                .widget-container h1 {{ font-size: 24px; }}
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="logo">KABUK</div>
            <div class="subtitle">AI-Powered Travel Intelligence</div>
        </div>

        <div class="main">
            <div class="widget-container">
                <h1>Meet Kyoko, Your Japan Travel Concierge</h1>
                <p>Chat with Kyoko about your Japan trip preferences. She has access to 10,230+ real traveler stories and can help you find the perfect stay.</p>

                <div class="elevenlabs-widget">
                    <!-- ElevenLabs Kyoko Agent Widget -->
                    <elevenlabs-convai agent-id="agent_0801kct0h5yyf6a84ss3yfn1b3ng"></elevenlabs-convai>
                </div>

                <a href="/details" class="details-link">📊 View API Details & Technical Info →</a>
            </div>
        </div>

        <div class="footer">
            © 2025 Kabuk International Inc. • Powered by ElevenLabs Conversational AI
        </div>

        <!-- ElevenLabs Widget Script -->
        <script src="https://unpkg.com/@elevenlabs/convai-widget-embed" async type="text/javascript"></script>
    </body>
    </html>
    """

def build_details_html():
    """Build technical details page"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>KABUK API - Technical Details</title>
        <meta charset="utf-8">
        <style>
            body {{ font-family: system-ui, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; background: #f5f5f5; }}
            .container {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            h1 {{ color: #333; }} h2 {{ color: #666; margin-top: 30px; }}
            .status {{ display: inline-block; padding: 4px 12px; background: #d4edda; color: #155724; border-radius: 4px; font-weight: bold; }}
            .endpoint {{ background: #f8f9fa; padding: 15px; margin: 10px 0; border-left: 4px solid #007bff; border-radius: 4px; }}
            .primary {{ border-left-color: #28a745; }}
            code {{ background: #f5f5f5; padding: 2px 6px; border-radius: 3px; font-family: monospace; }}
            pre {{ background: #f5f5f5; padding: 15px; border-radius: 4px; overflow-x: auto; }}
            .stats {{ display: flex; gap: 20px; margin: 20px 0; }}
            .stat {{ flex: 1; background: #e7f3ff; padding: 15px; border-radius: 4px; text-align: center; }}
            .stat-value {{ font-size: 24px; font-weight: bold; color: #007bff; }}
            .stat-label {{ font-size: 14px; color: #666; margin-top: 5px; }}
            .back-link {{ display: inline-block; margin-bottom: 20px; color: #8B5CF6; text-decoration: none; }}
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-link">← Back to Chat</a>
            <h1>🏨 KABUK API</h1>
            <p>ElevenLabs Agent Integration • Real-time property data from 10,230+ travel stories</p>
            <div class="status">🟢 LIVE</div>

            <div class="stats">
                <div class="stat">
                    <div class="stat-value">10,230</div>
                    <div class="stat-label">Travel Stories</div>
                </div>
                <div class="stat">
                    <div class="stat-value">1,630</div>
                    <div class="stat-label">Unique Properties</div>
                </div>
                <div class="stat">
                    <div class="stat-value">47,041</div>
                    <div class="stat-label">Property Images</div>
                </div>
                <div class="stat">
                    <div class="stat-value">13,013</div>
                    <div class="stat-label">Guest Likes</div>
                </div>
                <div class="stat">
                    <div class="stat-value">48</div>
                    <div class="stat-label">Countries</div>
                </div>
                <div class="stat">
                    <div class="stat-value">5</div>
                    <div class="stat-label">API Endpoints</div>
                </div>
            </div>

            <div class="stats" style="margin-top: 10px;">
                <div class="stat" style="flex: 1; font-size: 12px;">
                    <div class="stat-label">Top Destinations</div>
                    <div style="text-align: left; padding: 5px 10px; line-height: 1.4;">
                        🏯 Tokyo (1,590) • 🌸 Osaka (1,307) • 🏖️ Okinawa (840)<br>
                        ❄️ Hokkaido (750) • ⛩️ Kyoto (691)
                    </div>
                </div>
            </div>

            <h2>🎯 Primary Endpoint (Use This!)</h2>
            <div class="endpoint primary">
                <strong>POST /recommend</strong> - Intelligent multi-source recommendations<br>
                <small>Automatically combines properties, experiences, and inspiration based on query context</small>
                <pre>curl -X POST /recommend -H "Content-Type: application/json" \\
  -d '{{"query":"peaceful mountain retreat with hot springs","destination":"nagano"}}'</pre>
            </div>

            <h2>📚 Additional Endpoints</h2>

            <div class="endpoint">
                <strong>POST /search</strong> - Property search<br>
                <small>Search by destination and style preferences</small>
            </div>

            <div class="endpoint">
                <strong>POST /experiences</strong> - Guest experiences<br>
                <small>Real guest reviews and stay stories</small>
            </div>

            <div class="endpoint">
                <strong>POST /inspiration</strong> - Popular stories<br>
                <small>Top-rated properties sorted by guest likes</small>
            </div>

            <div class="endpoint">
                <strong>POST /gallery</strong> - Photo showcase<br>
                <small>Visual inspiration from property images</small>
            </div>

            <h2>🔧 Integration Demo</h2>
            <p>This POC demonstrates:</p>
            <ul>
                <li>✅ Real-time webhook integration with ElevenLabs voice AI</li>
                <li>✅ Multi-source data aggregation (properties + experiences + stories)</li>
                <li>✅ Intelligent endpoint selection based on conversation context</li>
                <li>✅ Japanese language support (10,230 real HafH travel stories)</li>
                <li>✅ Scalable architecture ready for production deployment</li>
            </ul>

            <h2>📈 Next Steps for Production</h2>
            <ul>
                <li>Deploy to production server (currently: Cloudflare tunnel)</li>
                <li>Add semantic search for better intent understanding</li>
                <li>Enhance with guest review quotes and property images</li>
                <li>Integrate with HafH booking/availability APIs</li>
                <li>Add authentication & rate limiting</li>
            </ul>

            <p style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 14px;">
                <strong>Technical Stack:</strong> Flask + ElevenLabs webhook integration with intelligent multi-source aggregation.
                This API combines property data, guest experiences, and travel stories to provide personalized recommendations.
            </p>
        </div>
    </body>
    </html>
    """

@app.route('/', methods=['GET'])
def index():
    """Landing page - cached for performance"""
    # Return cached HTML with performance headers
    response = app.make_response(CACHED_INDEX_HTML)
    response.headers['Cache-Control'] = 'public, max-age=300'  # Cache for 5 minutes
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/details', methods=['GET'])
def details():
    """Technical details and API documentation"""
    response = app.make_response(build_details_html())
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/favicon.ico', methods=['GET'])
def favicon():
    """Return 204 No Content for favicon to prevent 404 errors"""
    return '', 204

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'properties_loaded': len(PROPERTIES),
        'endpoints': {
            '/recommend': 'MAIN - Intelligent recommendations (use this!)',
            '/search': 'Property search',
            '/experiences': 'Guest experiences and reviews',
            '/inspiration': 'Popular travel stories',
            '/gallery': 'Photo-rich stays'
        }
    })

@app.route('/search', methods=['POST'])
def search_properties():
    """
    Search endpoint for ElevenLabs agent
    Expected format from agent: {"destination": "Kyoto", "style": "peaceful"}
    """
    try:
        data = request.get_json()
        destination = data.get('destination', '').lower() if data.get('destination') else ''
        style = data.get('style', '').lower() if data.get('style') else ''

        # For POC, return random selection if no specific match
        # In production, this would use semantic search with Sema
        results = []

        # Try to match based on any criteria
        for prop in PROPERTIES:
            match = False

            # Match destination in name/prefecture (handles Japanese and English)
            if destination:
                name_lower = prop['name'].lower() if prop['name'] else ''
                pref_lower = prop['prefecture'].lower() if prop['prefecture'] else ''
                if destination in name_lower or destination in pref_lower:
                    match = True

            # Match style in description
            if style:
                desc_lower = prop['description'].lower() if prop['description'] else ''
                if style in desc_lower:
                    match = True

            # If no filters specified, include all
            if not destination and not style:
                match = True

            if match:
                results.append(prop)

        # If no matches found, return a random sample for demo
        if not results and (destination or style):
            results = random.sample(PROPERTIES, min(5, len(PROPERTIES)))

        # Limit to top 5
        results = results[:5]

        # Format response for agent
        if results:
            summary = f"Found {len(results)} properties"
            if destination:
                summary += f" in {destination.title()}"

            property_list = []
            for prop in results:
                property_list.append({
                    'name': prop['name'],
                    'location': f"{prop['prefecture']}, {prop['country']}",
                    'highlight': prop['description'][:150] + '...' if len(prop['description']) > 150 else prop['description'],
                    'popularity': f"{prop['likes']} likes"
                })

            return jsonify({
                'success': True,
                'summary': summary,
                'properties': property_list,
                'count': len(results)
            })
        else:
            return jsonify({
                'success': True,
                'summary': 'No properties found matching your criteria',
                'properties': [],
                'count': 0
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/experiences', methods=['POST'])
def search_experiences():
    """
    Guest experiences endpoint - detailed reviews and stays
    Expected format: {"theme": "onsen", "prefecture": "nagano"}
    """
    try:
        data = request.get_json()
        theme = data.get('theme', '').lower() if data.get('theme') else ''
        prefecture = data.get('prefecture', '').lower() if data.get('prefecture') else ''

        results = []
        for prop in PROPERTIES:
            match = False

            # Match theme in description
            if theme:
                desc_lower = prop['description'].lower() if prop['description'] else ''
                if theme in desc_lower:
                    match = True

            # Match prefecture
            if prefecture:
                pref_lower = prop['prefecture'].lower() if prop['prefecture'] else ''
                if prefecture in pref_lower:
                    match = True

            if match or (not theme and not prefecture):
                results.append(prop)

        if not results and (theme or prefecture):
            results = random.sample(PROPERTIES, min(3, len(PROPERTIES)))

        results = results[:3]  # Limit to 3 for detailed experiences

        if results:
            experiences = []
            for prop in results:
                experiences.append({
                    'property': prop['name'],
                    'location': prop['prefecture'],
                    'experience': prop['description'],
                    'engagement': f"{prop['likes']} guests loved this"
                })

            return jsonify({
                'success': True,
                'summary': f"Found {len(experiences)} guest experiences",
                'experiences': experiences
            })
        else:
            return jsonify({
                'success': True,
                'summary': 'No experiences found',
                'experiences': []
            })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/inspiration', methods=['POST'])
def get_inspiration():
    """
    Popular stories endpoint - top-rated for inspiration
    Expected format: {"destination": "kyoto", "limit": 5}
    """
    try:
        data = request.get_json()
        destination = data.get('destination', '').lower() if data.get('destination') else ''
        limit = data.get('limit', 5)

        # Filter by destination if specified
        filtered = PROPERTIES
        if destination:
            filtered = [p for p in PROPERTIES
                       if destination in p['prefecture'].lower() or
                          destination in p['name'].lower()]

        # Sort by popularity (likes)
        popular = sorted(filtered, key=lambda x: x['likes'], reverse=True)[:limit]

        if not popular:
            popular = random.sample(PROPERTIES, min(limit, len(PROPERTIES)))

        stories = []
        for prop in popular:
            stories.append({
                'title': f"Stay at {prop['name']}",
                'location': prop['prefecture'],
                'snippet': prop['description'][:100] + '...' if len(prop['description']) > 100 else prop['description'],
                'popularity': f"⭐ {prop['likes']} likes"
            })

        return jsonify({
            'success': True,
            'summary': f"Here are {len(stories)} inspiring travel stories",
            'stories': stories
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/gallery', methods=['POST'])
def get_gallery():
    """
    Photo gallery endpoint - visual inspiration
    Expected format: {"style": "modern", "count": 4}
    """
    try:
        data = request.get_json()
        style = data.get('style', '').lower() if data.get('style') else ''
        count = data.get('count', 4)

        # For POC, return random properties
        # In production, would filter by properties with images
        results = random.sample(PROPERTIES, min(count, len(PROPERTIES)))

        gallery = []
        for prop in results:
            gallery.append({
                'property': prop['name'],
                'location': prop['prefecture'],
                'description': prop['description'][:80] + '...' if len(prop['description']) > 80 else prop['description'],
                'note': 'Photo gallery available in production'
            })

        return jsonify({
            'success': True,
            'summary': f"Visual showcase of {len(gallery)} properties",
            'gallery': gallery
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/recommend', methods=['POST'])
def intelligent_recommend():
    """
    Universal recommendation endpoint - intelligently combines all data sources
    Expected format: {"query": "I want a peaceful mountain retreat with onsen", "preferences": {...}}

    This is the PRIMARY endpoint the agent should use - it automatically determines
    which data sources to pull from based on the query context.
    """
    try:
        # DETAILED LOGGING FOR DEBUGGING
        print("\n" + "="*80)
        print("🔔 INCOMING /recommend REQUEST")
        print("="*80)
        print(f"Headers: {dict(request.headers)}")
        print(f"Raw data: {request.get_data(as_text=True)}")

        data = request.get_json()
        print(f"Parsed JSON: {data}")
        query = data.get('query', '').lower()
        destination = data.get('destination', '').lower() if data.get('destination') else ''
        print(f"Query: '{query}'")
        print(f"Destination: '{destination}'")

        response = {
            'success': True,
            'understanding': '',
            'recommendations': {}
        }

        # Analyze query intent
        is_looking_for_property = any(word in query for word in ['stay', 'hotel', 'property', 'where', 'visit'])
        wants_experiences = any(word in query for word in ['experience', 'review', 'guests', 'people say'])
        wants_inspiration = any(word in query for word in ['inspire', 'ideas', 'popular', 'recommend'])

        # If no specific signals, default to comprehensive response
        if not any([is_looking_for_property, wants_experiences, wants_inspiration]):
            is_looking_for_property = True
            wants_inspiration = True

        # Build understanding
        intent_parts = []
        if is_looking_for_property:
            intent_parts.append("properties")
        if wants_experiences:
            intent_parts.append("guest experiences")
        if wants_inspiration:
            intent_parts.append("travel inspiration")

        response['understanding'] = f"Looking for: {', '.join(intent_parts)}"

        # Get properties if requested
        if is_looking_for_property:
            props = []
            for prop in PROPERTIES:
                if destination:
                    if destination in prop['prefecture'].lower() or destination in prop['name'].lower():
                        props.append(prop)
                else:
                    # Match query keywords in description
                    if any(word in prop['description'].lower() for word in query.split() if len(word) > 3):
                        props.append(prop)

            if not props:
                props = random.sample(PROPERTIES, min(3, len(PROPERTIES)))

            response['recommendations']['properties'] = [{
                'name': p['name'],
                'location': p['prefecture'],
                'highlight': p['description'][:100] + '...' if len(p['description']) > 100 else p['description']
            } for p in props[:3]]

        # Get experiences if requested
        if wants_experiences:
            exp = random.sample(PROPERTIES, min(2, len(PROPERTIES)))
            response['recommendations']['experiences'] = [{
                'property': e['name'],
                'guest_story': e['description'][:150] + '...' if len(e['description']) > 150 else e['description'],
                'engagement': f"{e['likes']} likes"
            } for e in exp]

        # Get inspiration if requested
        if wants_inspiration:
            popular = sorted(PROPERTIES, key=lambda x: x['likes'], reverse=True)[:3]
            response['recommendations']['inspiration'] = [{
                'title': f"Popular: {p['name']}",
                'location': p['prefecture'],
                'why': "Highly rated by guests",
                'likes': p['likes']
            } for p in popular]

        print(f"✅ Response: {json.dumps(response, ensure_ascii=False)[:200]}...")
        print("="*80 + "\n")
        return jsonify(response)

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print("="*80 + "\n")
        return jsonify({'success': False, 'error': str(e)}), 500

# Load data at module import time (works with both gunicorn and direct run)
print("🚀 Starting HafH webhook server...")
load_sample_data()

# Build and cache landing page HTML for fast delivery
CACHED_INDEX_HTML = build_index_html()
print("✅ Landing page cached")

print(f"📊 Serving {len(PROPERTIES)} properties")

if __name__ == '__main__':
    print("🌐 Server running on http://localhost:5001")
    print("🔍 Search endpoint: POST http://localhost:5001/search")
    app.run(host='0.0.0.0', port=5001, debug=False)
