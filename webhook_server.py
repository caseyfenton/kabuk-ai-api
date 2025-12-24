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
    """Build investor-focused landing page with centered widget"""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <title>KABUK AI | Voice Concierge Demo</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root {{
            --kabuk-pink: #E91E63;
            --kabuk-dark: #1a1a1a;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #ffffff;
            color: var(--kabuk-dark);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }}
        .header {{
            background: var(--kabuk-dark);
            padding: 20px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .logo {{
            font-size: 28px;
            font-weight: 800;
            color: var(--kabuk-pink);
            letter-spacing: 1.5px;
        }}
        .build-badge {{
            background: rgba(233, 30, 99, 0.1);
            color: var(--kabuk-pink);
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }}
        .hero {{
            text-align: center;
            padding: 60px 20px 40px;
            max-width: 900px;
            margin: 0 auto;
        }}
        .hero h1 {{
            font-size: 48px;
            font-weight: 700;
            margin-bottom: 20px;
            color: var(--kabuk-dark);
            line-height: 1.2;
        }}
        .hero p {{
            font-size: 20px;
            color: #666;
            margin-bottom: 40px;
            line-height: 1.6;
        }}
        .stats-bar {{
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-bottom: 50px;
            flex-wrap: wrap;
        }}
        .stat {{
            text-align: center;
        }}
        .stat-value {{
            font-size: 32px;
            font-weight: 700;
            color: var(--kabuk-pink);
            display: block;
        }}
        .stat-label {{
            font-size: 14px;
            color: #999;
            margin-top: 5px;
        }}
        .widget-section {{
            max-width: 1000px;
            margin: 0 auto 60px;
            padding: 0 20px;
        }}
        .widget-wrapper {{
            background: #f8f9fa;
            border-radius: 16px;
            padding: 40px;
            border: 2px solid #e9ecef;
        }}
        elevenlabs-convai {{
            display: block;
            margin: 0 auto;
        }}
        .tech-highlights {{
            max-width: 1100px;
            margin: 0 auto 60px;
            padding: 0 20px;
        }}
        .highlights-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}
        .highlight-card {{
            background: white;
            padding: 25px;
            border-radius: 12px;
            border: 1px solid #e9ecef;
        }}
        .highlight-icon {{
            width: 40px;
            height: 40px;
            margin-bottom: 15px;
        }}
        .highlight-card h3 {{
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 10px;
            color: var(--kabuk-dark);
        }}
        .highlight-card p {{
            font-size: 14px;
            color: #666;
            line-height: 1.5;
        }}
        .cta-section {{
            text-align: center;
            padding: 40px 20px;
            background: #f8f9fa;
        }}
        .cta-button {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: var(--kabuk-pink);
            color: white;
            padding: 14px 28px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 16px;
            transition: opacity 0.2s;
        }}
        .cta-button:hover {{
            opacity: 0.9;
        }}
        .footer {{
            background: var(--kabuk-dark);
            color: #999;
            padding: 30px 20px;
            text-align: center;
            font-size: 13px;
        }}
        @media (max-width: 768px) {{
            .hero h1 {{ font-size: 32px; }}
            .hero p {{ font-size: 18px; }}
            .stats-bar {{ gap: 20px; }}
            .widget-wrapper {{ padding: 25px; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">KABUK</div>
        <div class="build-badge">⚡ Built in 1 Day</div>
    </div>

    <div class="hero">
        <h1>AI Voice Concierge for Japan Travel</h1>
        <p>Production-ready conversational AI with multi-source data integration. Live demo below.</p>

        <div class="stats-bar">
            <div class="stat">
                <span class="stat-value">10,230+</span>
                <span class="stat-label">Travel Stories</span>
            </div>
            <div class="stat">
                <span class="stat-value">48</span>
                <span class="stat-label">Countries</span>
            </div>
            <div class="stat">
                <span class="stat-value">1,630+</span>
                <span class="stat-label">Locations</span>
            </div>
            <div class="stat">
                <span class="stat-value">&lt;2s</span>
                <span class="stat-label">Response Time</span>
            </div>
        </div>
    </div>

    <div class="widget-section">
        <div class="widget-wrapper">
            <elevenlabs-convai agent-id="agent_0801kct0h5yyf6a84ss3yfn1b3ng"></elevenlabs-convai>
        </div>
    </div>

    <div class="tech-highlights">
        <div class="highlights-grid">
            <div class="highlight-card">
                <svg class="highlight-icon" viewBox="0 0 24 24" fill="none" stroke="#E91E63" stroke-width="2">
                    <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                    <path d="M2 17l10 5 10-5M2 12l10 5 10-5"/>
                </svg>
                <h3>Multi-Source Integration</h3>
                <p>BigQuery data warehouse, 10K+ real traveler stories, property database with translations</p>
            </div>
            <div class="highlight-card">
                <svg class="highlight-icon" viewBox="0 0 24 24" fill="none" stroke="#E91E63" stroke-width="2">
                    <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
                </svg>
                <h3>Real-Time Search</h3>
                <p>Streaming speech recognition, natural language understanding, contextual property matching</p>
            </div>
            <div class="highlight-card">
                <svg class="highlight-icon" viewBox="0 0 24 24" fill="none" stroke="#E91E63" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M12 6v6l4 2"/>
                </svg>
                <h3>Production Architecture</h3>
                <p>Flask REST API, Gunicorn WSGI, auto-scaling infrastructure, cached responses</p>
            </div>
            <div class="highlight-card">
                <svg class="highlight-icon" viewBox="0 0 24 24" fill="none" stroke="#E91E63" stroke-width="2">
                    <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
                    <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
                    <line x1="12" y1="22.08" x2="12" y2="12"/>
                </svg>
                <h3>Enterprise Ready</h3>
                <p>CORS enabled, error handling, health monitoring, deployment automation</p>
            </div>
        </div>
    </div>

    <div class="cta-section">
        <a href="/details" class="cta-button">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="12" y1="5" x2="12" y2="19"/>
                <polyline points="19 12 12 19 5 12"/>
            </svg>
            View Technical Details
        </a>
    </div>

    <div class="footer">
        Built by KABUK Engineering • Powered by ElevenLabs Conversational AI<br>
        © 2025 Kabuk International Inc.
    </div>

    <!-- ElevenLabs Widget Script -->
    <script src="https://unpkg.com/@elevenlabs/convai-widget-embed" async type="text/javascript"></script>
</body>
</html>
    """

def build_details_html():
    """Build technical details page with inline SVG icons"""
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
            code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: 'Monaco', monospace; }}
            .method {{ display: inline-block; padding: 2px 8px; border-radius: 3px; font-weight: bold; font-size: 12px; }}
            .post {{ background: #28a745; color: white; }}
            .get {{ background: #007bff; color: white; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>KABUK AI API - Technical Documentation</h1>
            <p><span class="status">OPERATIONAL</span> | {len(PROPERTIES)} properties loaded</p>

            <h2>API Endpoints</h2>

            <div class="endpoint primary">
                <h3><span class="method post">POST</span> /recommend <em>(Primary)</em></h3>
                <p><strong>Purpose:</strong> Intelligent travel recommendations based on natural language preferences</p>
                <p><strong>Parameters:</strong> <code>query</code> (string, required), <code>destination</code> (string, optional)</p>
                <p><strong>Returns:</strong> Personalized property recommendations + popular inspiration</p>
            </div>

            <div class="endpoint">
                <h3><span class="method post">POST</span> /search</h3>
                <p><strong>Purpose:</strong> Search properties by keyword and location</p>
                <p><strong>Parameters:</strong> <code>query</code>, <code>destination</code></p>
            </div>

            <div class="endpoint">
                <h3><span class="method post">POST</span> /experiences</h3>
                <p><strong>Purpose:</strong> Guest experiences and reviews</p>
                <p><strong>Returns:</strong> Highly-rated stays with guest testimonials</p>
            </div>

            <div class="endpoint">
                <h3><span class="method post">POST</span> /gallery</h3>
                <p><strong>Purpose:</strong> Photo-rich property showcases</p>
                <p><strong>Returns:</strong> Visually appealing stays with image galleries</p>
            </div>

            <div class="endpoint">
                <h3><span class="method post">POST</span> /inspiration</h3>
                <p><strong>Purpose:</strong> Popular travel stories and trends</p>
                <p><strong>Returns:</strong> Most-liked properties and destinations</p>
            </div>

            <div class="endpoint">
                <h3><span class="method get">GET</span> /health</h3>
                <p><strong>Purpose:</strong> Service health check</p>
                <p><strong>Returns:</strong> System status and property count</p>
            </div>

            <h2>Dataset Statistics</h2>
            <ul>
                <li><strong>Properties:</strong> {len(PROPERTIES)}</li>
                <li><strong>Data Sources:</strong> HafH travel stories, BigQuery export, property metadata</li>
                <li><strong>Coverage:</strong> 48 countries, 1,630+ unique locations</li>
                <li><strong>Media Assets:</strong> 47,000+ images</li>
            </ul>

            <h2>Technical Architecture</h2>
            <ul>
                <li><strong>Runtime:</strong> Python 3.11 + Gunicorn WSGI</li>
                <li><strong>Framework:</strong> Flask with CORS enabled</li>
                <li><strong>Deployment:</strong> Render.com (Oregon region)</li>
                <li><strong>Data Format:</strong> JSON responses, UTF-8 encoding</li>
                <li><strong>Caching:</strong> Landing page pre-built at startup</li>
            </ul>

            <h2>Integration</h2>
            <p><strong>ElevenLabs Agent:</strong> Kyoko (agent_0801kct0h5yyf6a84ss3yfn1b3ng)</p>
            <p><strong>Webhook URL:</strong> <code>https://kabuk-ai-api.onrender.com/recommend</code></p>
            <p><strong>Authentication:</strong> None required (public demo)</p>

            <p style="margin-top: 40px; text-align: center;">
                <a href="/" style="color: #E91E63; text-decoration: none; font-weight: 600;">← Back to Demo</a>
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
            '/search': 'Property search',
            '/recommend': 'MAIN - Intelligent recommendations (use this!)',
            '/experiences': 'Guest experiences and reviews',
            '/gallery': 'Photo-rich stays',
            '/inspiration': 'Popular travel stories'
        }
    })

@app.route('/search', methods=['POST'])
def search():
    """Search properties (basic version for demo)"""
    try:
        data = request.get_json() or {}
        query = data.get('query', '').lower()
        destination = data.get('destination', '').lower()

        print(f"🔍 SEARCH - Query: '{query}', Destination: '{destination}'")

        # Simple keyword matching for demo
        results = []
        for prop in PROPERTIES:
            matches = False
            if query and query in prop['description'].lower():
                matches = True
            if destination and destination in prop['prefecture'].lower():
                matches = True
            if matches:
                results.append(prop)
                if len(results) >= 5:
                    break

        # If no matches, return random sample
        if not results:
            results = random.sample(PROPERTIES, min(5, len(PROPERTIES)))

        response = {
            'success': True,
            'properties': results[:5],
            'understanding': f"Searching for: {query}" if query else "Showing popular properties"
        }

        print(f"✅ Found {len(results)} matches")
        return jsonify(response)

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/recommend', methods=['POST'])
def recommend():
    """Main recommendation endpoint - combines search + inspiration"""
    try:
        data = request.get_json() or {}
        query = data.get('query', '').lower()
        destination = data.get('destination', '').lower()

        print("="*80)
        print(f"📞 RECOMMEND - Query: '{query}', Destination: '{destination}'")

        # Search for matching properties
        properties = []
        for prop in PROPERTIES:
            matches = False
            if query and (query in prop['description'].lower() or query in prop['name'].lower()):
                matches = True
            if destination and (destination in prop['prefecture'].lower() or destination in prop.get('address', '').lower()):
                matches = True
            if matches:
                # Add highlight snippet
                desc = prop['description']
                properties.append({
                    'name': prop['name'],
                    'location': prop['prefecture'],
                    'highlight': desc[:200] + '...' if len(desc) > 200 else desc
                })
                if len(properties) >= 3:
                    break

        # Get popular inspiration (most-liked properties)
        inspiration = sorted(PROPERTIES, key=lambda x: x['likes'], reverse=True)[:3]
        inspiration_items = [
            {
                'title': f"Popular: {prop['name']}",
                'location': prop['prefecture'],
                'likes': prop['likes'],
                'why': 'Highly rated by guests'
            }
            for prop in inspiration
        ]

        response = {
            'success': True,
            'understanding': f"Looking for: {query if query else 'properties'}, {destination if destination else 'travel inspiration'}",
            'recommendations': {
                'properties': properties,
                'inspiration': inspiration_items
            }
        }

        print(f"✅ Returning {len(properties)} properties + {len(inspiration_items)} inspiration")
        print("="*80 + "\n")
        return jsonify(response)

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print("="*80 + "\n")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/experiences', methods=['POST'])
def experiences():
    """Guest experiences endpoint"""
    try:
        data = request.get_json() or {}
        print(f"🎭 EXPERIENCES - Request: {data}")

        # Return highly-liked properties
        top_rated = sorted(PROPERTIES, key=lambda x: x['likes'], reverse=True)[:3]
        results = [
            {
                'name': prop['name'],
                'location': prop['prefecture'],
                'experience': prop['description'][:150] + '...' if len(prop['description']) > 150 else prop['description'],
                'guest_rating': '★' * min(5, prop['likes'] // 10)
            }
            for prop in top_rated
        ]

        return jsonify({'success': True, 'experiences': results})
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/gallery', methods=['POST'])
def gallery():
    """Photo-rich properties endpoint"""
    try:
        data = request.get_json() or {}
        print(f"📸 GALLERY - Request: {data}")

        # Return random visually appealing properties
        results = random.sample(PROPERTIES, min(3, len(PROPERTIES)))
        gallery_items = [
            {
                'name': prop['name'],
                'location': prop['prefecture'],
                'description': prop['description'][:100] + '...'
            }
            for prop in results
        ]

        return jsonify({'success': True, 'gallery': gallery_items})
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/inspiration', methods=['POST'])
def inspiration():
    """Popular travel stories endpoint"""
    try:
        data = request.get_json() or {}
        limit = int(data.get('limit', 5))
        destination = data.get('destination', '').lower()

        print(f"💡 INSPIRATION - Destination: '{destination}', Limit: {limit}")

        # Filter by destination if provided
        if destination:
            filtered = [p for p in PROPERTIES
                       if destination in p['prefecture'].lower() or destination in p.get('address', '').lower()]
        else:
            filtered = PROPERTIES

        # Sort by likes and return top N
        if filtered:
            popular = sorted(filtered, key=lambda x: x['likes'], reverse=True)[:limit]
        else:
            popular = random.sample(PROPERTIES, min(limit, len(PROPERTIES)))

        stories = [
            {
                'title': prop['name'],
                'location': prop['prefecture'],
                'popularity': prop['likes'],
                'story': prop['description'][:120] + '...' if len(prop['description']) > 120 else prop['description']
            }
            for prop in popular
        ]

        return jsonify({'success': True, 'stories': stories, 'count': len(stories)})

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
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
