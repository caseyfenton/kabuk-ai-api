# 5-Minute Deployment to Render.com

**Total Time**: 5 minutes
**Cost**: $0 (free tier)
**Size**: 23.2MB

---

## Pre-Deployment Checklist

✅ All tests passed (`python3 test_local.py`)
✅ Hardcoded paths fixed (uses relative paths)
✅ Dependencies included (Flask, Flask-CORS, Gunicorn)
✅ Data file included (10,230 properties, 23MB)
✅ Total size 23.2MB (well under 512MB free tier limit)

---

## Deploy in 2 Steps

### Step 1: Prepare Package (1 minute)

```bash
cd /Users/casey/pro/KABUK/render-deploy

# Initialize git (for version control)
git init
git add .
git commit -m "Deploy KABUK AI API to Render"
```

### Step 2: Deploy on Render (3 minutes)

**Option A: Manual Configuration**

1. Go to https://dashboard.render.com/
2. Click **"New +"** → **"Web Service"**
3. Choose **"Deploy an existing image or repository"**
4. Select **"Public Git repository"** or upload directory as ZIP
5. **Manual Settings**:
   - **Name**: kabuk-ai-api
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn webhook_server:app`
   - **Environment Variables**:
     - `PYTHON_VERSION` = `3.11.0`
6. Click **"Create Web Service"**

**Option B: Auto-Configuration** (if render.yaml detected)

1. Upload directory or connect repository
2. Render auto-detects `render.yaml` config
3. Click **"Create Web Service"**

**Build takes ~2 minutes**. Watch for:
- ✅ "Installing dependencies..."
- ✅ "Starting server..."
- ✅ "Loaded 10230 properties"

### Step 3: Update ElevenLabs (1 minute)

1. Go to ElevenLabs Agent Dashboard
2. Open "Hana" agent configuration
3. Edit "Client Tools" → "KABUK_POC" webhook
4. Change URL to:
   ```
   https://kabuk-ai-api.onrender.com/recommend
   ```
5. Save configuration

**Done!** Your webhook is live at: `https://kabuk-ai-api.onrender.com`

---

## Test the Deployment

```bash
# Test health endpoint
curl https://kabuk-ai-api.onrender.com/health

# Expected output:
# {"status":"healthy","properties_loaded":10230,...}

# Test recommendation endpoint
curl -X POST https://kabuk-ai-api.onrender.com/recommend \
  -H "Content-Type: application/json" \
  -d '{"query":"peaceful mountain onsen","destination":"nagano"}'

# Expected: JSON with properties, experiences, inspiration
```

---

## What Gets Deployed

```
📦 kabuk-ai-api (23.2MB)
├── webhook_server.py      # Flask API server
├── data/
│   └── hafh_stories.json  # 10,230 travel stories
├── static/                # HTML demo pages
├── requirements.txt       # Python dependencies
├── render.yaml           # Auto-config for Render
└── README.md             # Full API docs
```

**What's NOT Included** (stays local):
- NDA documents
- Interview transcripts
- BigQuery exports
- Client communications

---

## Free Tier Limits

| Resource | Limit | Used | Available |
|----------|-------|------|-----------|
| Disk | 512MB | 75MB | 437MB |
| RAM | 512MB | ~100MB | ~400MB |
| Bandwidth | 100GB/mo | ~1GB/mo | 99GB |
| Build Time | 15 min | 2 min | 13 min |

**Limitation**: Service sleeps after 15min idle
- First request after sleep: ~30s (cold start)
- All other requests: <500ms

**Upgrade to $7/mo Starter**: Always-on, no cold starts

---

## Monitoring

**View Logs**:
1. Dashboard → Select service → "Logs" tab
2. Watch for webhook requests: `🔔 INCOMING /recommend REQUEST`

**Check Health**:
```bash
curl https://kabuk-ai-api.onrender.com/health
```

**Monitor Metrics**:
- Dashboard shows CPU, RAM, response time
- Should see: <10% CPU idle, ~100MB RAM baseline

---

## Troubleshooting

### Build Failed
**Check**: Build logs in Render dashboard
**Common**: Python version mismatch, missing dependencies
**Fix**: Verify `render.yaml` has `PYTHON_VERSION: 3.11.0`

### 404 Not Found
**Check**: Service is "Live" (not "Build Failed")
**Common**: Gunicorn not starting webhook_server:app
**Fix**: Verify `startCommand` in render.yaml

### Data Not Loading
**Check**: Logs for "⚠️ Could not load data"
**Common**: data/hafh_stories.json missing from upload
**Fix**: Verify file exists: `ls -lh data/`

### Slow Responses
**Check**: First request >5s? (Cold start after 15min idle)
**Common**: Free tier sleeps after inactivity
**Fix**: Upgrade to $7/mo Starter plan (always-on)

---

## Next Actions

**Immediate**:
1. Share URL with team
2. Test ElevenLabs conversation flow
3. Monitor logs for first 24 hours

**Short-term**:
1. Add semantic search (Sema integration)
2. Upgrade to Starter plan if >10 calls/day
3. Implement request logging for analytics

**Production**:
1. Add authentication (API keys)
2. Implement rate limiting
3. Move to PostgreSQL database
4. Add Redis caching

---

## Support

**Render**: https://render.com/docs
**Status**: https://status.render.com/
**Project Docs**: See README.md for full API docs
**Full Deployment Guide**: See RENDER_DEPLOYMENT.md

---

**Ready to Deploy?** Run:
```bash
cd /Users/casey/pro/KABUK/render-deploy
python3 test_local.py  # Verify package
# Then follow Step 1 above
```
