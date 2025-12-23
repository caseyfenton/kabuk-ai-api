# KABUK Webhook API - Render.com Deployment

Production-ready Flask webhook server for ElevenLabs voice AI integration with KABUK travel stories database.

## What's Included

- **webhook_server.py** - Flask server with 5 API endpoints (23MB total deployment)
- **data/hafh_stories.json** - Complete KABUK travel stories database (10,230 properties)
- **static/** - HTML demo pages (property carousel, testing interface)
- **requirements.txt** - Python dependencies (Flask, Flask-CORS, Gunicorn)
- **render.yaml** - Render.com infrastructure config

## Deployment Size

**Total: 23MB** - Well within Render free tier limits (512MB disk)

**Breakdown:**
- Data file: 23MB (hafh_stories.json)
- Code: <1MB (Python + HTML)
- Dependencies: ~50MB installed (Flask, Gunicorn)

## Render Free Tier Limits

✅ **Fits comfortably in free tier:**
- Disk: 512MB limit (we use ~75MB total)
- RAM: 512MB (Flask uses ~100MB)
- Build time: 15 minutes (we build in ~2 min)
- Service spins down after 15min inactivity (restarts in ~30s)

## Quick Deploy to Render.com

### Deploy to Render.com

