# KABUK AI API - Demo Notes for Jeffrey

## Render.com Deployment Status
**Live URL**: `https://kabuk-ai-api.onrender.com/recommend`
**Dataset**: 10,230 travel stories loaded and searchable
**Region**: Oregon (US West Coast)

---

## Important: Cold Start Behavior (Free Tier)

### What Happens
Render's free tier **sleeps after 15 minutes of inactivity** to save resources. When first request arrives after sleep:
- **First request**: ~30 seconds to wake up + respond
- **All subsequent requests**: <500ms (normal speed)

### Before Live Demo
**Warm up the service** 5 minutes before demo:
```bash
curl https://kabuk-ai-api.onrender.com/health
```
Or simply visit the URL in browser. This wakes it up so demo runs smoothly.

### During Demo
- First interaction may have slight delay if service was sleeping
- After first response, all interactions will be fast
- Set expectation: "The AI is thinking..." covers the warm-up

### For Production Use
If cold starts become problematic:
- **Upgrade to Starter plan**: $7/month
- **Benefit**: Always-on, no cold starts, 5x faster CPU
- **When to upgrade**: If getting >10 calls/day or need instant response

---

## ElevenLabs Integration

### Current Webhook Configuration
**Tool Name**: KABUK_POC
**URL**: `https://kabuk-ai-api.onrender.com/recommend`
**Method**: POST
**Parameters**:
- `query` (required): Natural language travel preferences
- `destination` (optional): Specific location/prefecture

### Test the Integration
1. Call the ElevenLabs agent (Hana)
2. Say: "I'm looking for a peaceful mountain retreat with hot springs in Nagano"
3. Agent extracts preferences and calls webhook
4. Returns property recommendations with descriptions

---

## Technical Details

### Free Tier Limits
| Resource | Limit | Usage | Status |
|----------|-------|-------|--------|
| Disk Space | 512MB | ~75MB | ✅ 85% free |
| RAM | 512MB | ~100MB | ✅ 80% free |
| Bandwidth | 100GB/mo | ~1GB/mo | ✅ 99% free |
| Build Time | 15 min | ~2 min | ✅ Well under |

### Monitoring
**Health Check**: `curl https://kabuk-ai-api.onrender.com/health`

**Expected Response**:
```json
{
  "status": "healthy",
  "properties_loaded": 10230,
  "endpoints": {
    "/recommend": "MAIN - Intelligent recommendations",
    "/search": "Property search",
    "/experiences": "Guest experiences and reviews",
    "/inspiration": "Popular travel stories",
    "/gallery": "Photo-rich stays"
  }
}
```

### Support
**Platform Status**: https://status.render.com/
**Dashboard**: https://dashboard.render.com/
**Documentation**: See RENDER_DEPLOYMENT.md for full guide

---

## Cost Summary
**Current**: $0/month (free tier)
**Optional Upgrade**: $7/month (always-on, no cold starts)
**Recommended**: Start free, upgrade if cold starts become issue
