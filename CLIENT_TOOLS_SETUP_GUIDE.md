# Client Tools Setup Guide - KABUK AI Kyoko Agent

**Created**: December 24, 2025
**Goal**: Enable voice + visual UX for Kyoko agent (Jan 1st deadline)
**Status**: Implementation ready, needs agent configuration

---

## Quick Start (5 Steps to Go Live)

### 1. Get Your Agent ID

1. Go to https://elevenlabs.io/app/conversational-ai
2. Find "Kyoko" agent (or create if doesn't exist)
3. Copy the **Agent ID** from settings
   - Format: `agent_xxxxxxxxxxxxxxxxxxxxx`
   - You'll need this for the HTML page

### 2. Update HTML Page with Agent ID

Edit `/static/kyoko-voice-demo.html` line 432:

```html
<!-- BEFORE -->
<elevenlabs-convai agent-id="YOUR_AGENT_ID_HERE"></elevenlabs-convai>

<!-- AFTER -->
<elevenlabs-convai agent-id="agent_ABC123XYZ"></elevenlabs-convai>
```

### 3. Configure Client Tools in ElevenLabs Dashboard

Go to your Kyoko agent → **Tools** tab → **Add Client Tool**

Create these 5 client tools:

#### Tool 1: showProperties

- **Name**: `showProperties` (EXACT - case sensitive)
- **Type**: Client
- **Description**: "Display property cards in the browser UI with images, names, locations, and descriptions based on user's travel preferences"
- **Parameters**:
  - `query` (string, required): "The search query or user preferences (e.g., 'mountain hot springs in Nagano')"
  - `properties` (array, required): "Array of property objects with fields: pid, name, prefecture, country, images, ts_stay_text, likes_count"
- **Wait for Response**: ✅ Enabled

#### Tool 2: highlightProperty

- **Name**: `highlightProperty` (EXACT)
- **Type**: Client
- **Description**: "Highlight a specific property card with visual emphasis and show reason why it's recommended"
- **Parameters**:
  - `propertyId` (string, required): "Property ID (pid) to highlight"
  - `reason` (string, optional): "Why this property is being highlighted (e.g., 'Best match for your mountain preference')"
- **Wait for Response**: ✅ Enabled

#### Tool 3: openPropertyDetail

- **Name**: `openPropertyDetail` (EXACT)
- **Type**: Client
- **Description**: "Open detailed modal view for a property showing full description, gallery, and booking info"
- **Parameters**:
  - `propertyId` (string, required): "Property ID (pid) to show details for"
- **Wait for Response**: ✅ Enabled

#### Tool 4: clearDisplay

- **Name**: `clearDisplay` (EXACT)
- **Type**: Client
- **Description**: "Clear all displayed properties from the screen when starting a new search"
- **Parameters**: None
- **Wait for Response**: ❌ Disabled (fire and forget)

#### Tool 5: showLoading

- **Name**: `showLoading` (EXACT)
- **Type**: Client
- **Description**: "Show loading spinner with custom message while processing long operations"
- **Parameters**:
  - `message` (string, optional): "Loading message to display (e.g., 'Finding perfect properties for you...')"
- **Wait for Response**: ❌ Disabled

### 4. Update Agent System Prompt

Add this section to Kyoko's system prompt (after existing personality/context):

```
## Visual Display Integration (IMPORTANT)

You have access to browser control via Client Tools. Use them to create a coordinated voice + visual experience:

### WORKFLOW:
1. User shares preferences → You call webhook to search properties
2. Webhook returns property data → You call showProperties() client tool to display them
3. You verbally describe 2-3 top recommendations
4. As you talk about each property, call highlightProperty() to draw visual attention
5. If user wants details, call openPropertyDetail()

### CRITICAL RULES:
- ALWAYS call showProperties() after webhook returns property data
- NEVER just describe properties verbally - show them visually too
- When highlighting a property, provide a clear reason parameter
- Keep voice short while visuals load (e.g., "Let me show you what I found")
- Call clearDisplay() before a new search to avoid confusion

### EXAMPLE FLOW:
User: "I want mountain hot springs in Nagano"
You: (internal) Call webhook tool to search
You: (after webhook returns) Call showProperties(query="mountain hot springs", properties=<webhook_data>)
You: (speak) "Perfect! I found 5 amazing mountain hot springs in Nagano. Let me walk you through the top 3..."
You: Call highlightProperty(propertyId="12345", reason="Best hot spring with mountain views")
You: (speak) "This one has incredible views and authentic rotenburo..."
You: Call highlightProperty(propertyId="67890", reason="Most affordable option")
You: (speak) "This ryokan offers great value with traditional tatami rooms..."

### CLIENT TOOLS AVAILABLE:
- showProperties(query, properties) - Display property cards
- highlightProperty(propertyId, reason) - Emphasize specific property
- openPropertyDetail(propertyId) - Show full details
- clearDisplay() - Clear screen for new search
- showLoading(message) - Show loading state

Use these tools proactively to create a seamless voice + visual experience.
```

### 5. Deploy and Test

1. Deploy updated HTML to Render.com:
   ```bash
   git add static/kyoko-voice-demo.html
   git commit -m "feat: Client Tools integration for voice + visual UX"
   git push
   ```

2. Visit: `https://kabuk-ai-api.onrender.com/kyoko-voice-demo.html`

3. Test conversation:
   - Click voice button
   - Say: "I want mountain hot springs in Nagano"
   - Kyoko should:
     1. Call webhook (backend)
     2. Call showProperties (frontend - displays cards)
     3. Verbally describe properties
     4. Call highlightProperty as she talks about each one

---

## Architecture Overview

### Current Flow (Voice Only)

```
User speaks → Agent → Webhook → Backend search → Agent speaks results
```

**Problem**: User only hears descriptions, no visual confirmation

### New Flow (Voice + Visual)

```
User speaks
   ↓
ElevenLabs Agent (Kyoko)
   ↓
1. Call webhook tool → backend search (10,230 properties)
   ↓
2. Call showProperties() → browser displays cards
   ↓
3. Speak results while visuals show
   ↓
4. Call highlightProperty() as you describe each property
   ↓
5. Call openPropertyDetail() if user wants more info
```

**Benefits**:
- User sees + hears recommendations simultaneously
- Visual feedback confirms agent understood preferences
- Highlighted properties draw attention to top matches
- Better engagement and trust

---

## Client Tools Technical Details

### How They Work

1. **Defined in HTML**: JavaScript functions in `kyoko-voice-demo.html`
2. **Registered with SDK**: `ElevenLabs.Conversation.registerClientTools(clientTools)`
3. **Called by Agent**: When agent decides to use them during conversation
4. **Execute in Browser**: Run client-side, update DOM directly
5. **Return Status**: Send success/failure back to agent

### Complete Client Tools Object

```javascript
const clientTools = {
    showProperties: async ({query, properties}) => {
        // 1. Hide empty state
        // 2. Show context banner with query
        // 3. Render property cards in grid
        // 4. Scroll to properties
        // 5. Return {success: true, count: X}
    },

    highlightProperty: async ({propertyId, reason}) => {
        // 1. Remove previous highlights
        // 2. Find property card by data-property-id
        // 3. Add 'highlight' class (border + shadow)
        // 4. Show reason badge if provided
        // 5. Scroll into view
        // 6. Return {success: true/false}
    },

    openPropertyDetail: async ({propertyId}) => {
        // 1. Find property in currentProperties array
        // 2. Build modal with full details
        // 3. Show image gallery
        // 4. Display modal
        // 5. Return {success: true}
    },

    clearDisplay: async () => {
        // 1. Clear properties container
        // 2. Hide context banner
        // 3. Show empty state
        // 4. Remove highlights
        // 5. Return {success: true}
    },

    showLoading: async ({message}) => {
        // 1. Show loading spinner
        // 2. Update loading message
        // 3. Return {success: true}
    }
};
```

### Data Flow Example

**User**: "Find me traditional Kyoto ryokans"

**1. Agent calls webhook tool**:
```json
{
  "tool": "KABUK_POC",
  "parameters": {
    "query": "traditional ryokan",
    "destination": "Kyoto"
  }
}
```

**2. Webhook returns**:
```json
{
  "properties": [
    {
      "pid": "12345",
      "name": "Gion Hatanaka",
      "prefecture": "Kyoto",
      "country": "JP",
      "images": ["https://..."],
      "ts_stay_text": "Beautiful traditional ryokan in Gion...",
      "likes_count": 234
    },
    // ... more properties
  ]
}
```

**3. Agent calls showProperties client tool**:
```javascript
clientTools.showProperties({
  query: "traditional Kyoto ryokans",
  properties: [/* 5 properties from webhook */]
})
```

**4. Browser displays cards**

**5. Agent speaks**: "I found 5 wonderful traditional ryokans in Kyoto..."

**6. Agent calls highlightProperty**:
```javascript
clientTools.highlightProperty({
  propertyId: "12345",
  reason: "Best location in historic Gion district"
})
```

**7. Browser highlights card with badge**

---

## Coordinating Webhook + Client Tools

### Agent Logic Pattern

```javascript
// Agent's internal decision flow (conceptual)

async function handleUserRequest(userMessage) {
    // 1. Extract preferences
    const preferences = extractPreferences(userMessage);
    // e.g., {destination: "Kyoto", style: "traditional", budget: "mid"}

    // 2. Call WEBHOOK tool (backend search)
    const webhookResult = await callTool("KABUK_POC", {
        query: preferences.style,
        destination: preferences.destination
    });

    // 3. Call CLIENT tool (frontend display)
    await callTool("showProperties", {
        query: `${preferences.style} accommodations in ${preferences.destination}`,
        properties: webhookResult.properties
    });

    // 4. Speak summary
    speak(`I found ${webhookResult.properties.length} beautiful properties...`);

    // 5. Highlight top pick
    const topPick = webhookResult.properties[0];
    await callTool("highlightProperty", {
        propertyId: topPick.pid,
        reason: "Best match for traditional Kyoto experience"
    });

    // 6. Describe highlighted property
    speak(`This ryokan in Gion district is perfect because...`);
}
```

### Key Principle

**Webhook** = Fetch data (backend, slow, hidden from user)
**Client Tools** = Show data (frontend, instant, visible to user)

Always pair them: Webhook → Client Tool

---

## Testing Checklist

### Local Testing

1. **Open page**: http://localhost:5001/kyoko-voice-demo.html
2. **Check console**: Should see "✅ Client Tools registered"
3. **Click voice button**: Agent widget should appear
4. **Start conversation**: "Show me mountain hot springs"
5. **Verify**:
   - [ ] Agent calls webhook (check backend logs)
   - [ ] Properties display on screen (showProperties works)
   - [ ] Context banner shows query
   - [ ] Agent describes properties verbally
   - [ ] Properties highlight as agent talks (highlightProperty works)

### Production Testing (Render.com)

1. **Deploy**: `git push` to trigger Render deployment
2. **Visit**: https://kabuk-ai-api.onrender.com/kyoko-voice-demo.html
3. **Run same test** as local
4. **Check Render logs**: Should see webhook calls
5. **Record demo**: Use Loom to capture voice + visual demo

### Edge Cases to Test

- [ ] No results found (empty properties array)
- [ ] Very long property descriptions (card overflow)
- [ ] Missing images (fallback placeholder)
- [ ] Highlighting non-existent property ID (should return error)
- [ ] Rapid tool calls (multiple highlights in quick succession)
- [ ] Mobile view (responsive design)

---

## Troubleshooting

### "Client Tools not working"

**Check**:
1. Agent ID in HTML matches your agent
2. Tool names in dashboard EXACTLY match code (case-sensitive)
3. Browser console shows "✅ Client Tools registered"
4. Agent system prompt includes Client Tools instructions

**Common mistake**: Tool name mismatch
- Dashboard: `ShowProperties` (capital S)
- Code: `showProperties` (lowercase s)
- **Must match exactly**

### "Properties not displaying"

**Check**:
1. Webhook is returning valid data (check network tab)
2. `properties` parameter is an array
3. Each property has required fields: `pid`, `name`, `images`
4. Console errors for JavaScript exceptions

**Debug**:
```javascript
// Add to showProperties function
console.log('Properties received:', properties);
console.log('First property:', properties[0]);
```

### "Highlight not working"

**Check**:
1. Property ID matches exactly (case-sensitive)
2. Property card has `data-property-id` attribute
3. CSS `highlight` class is defined

**Debug**:
```javascript
// Add to highlightProperty function
console.log('Looking for property:', propertyId);
const card = document.querySelector(`[data-property-id="${propertyId}"]`);
console.log('Found card:', card);
```

### "Agent not calling client tools"

**Check**:
1. System prompt includes Client Tools usage instructions
2. Tools are enabled in agent settings
3. Agent has permission to use client tools (not blocked by plan)

**Test manually**:
```javascript
// In browser console
await clientTools.showProperties({
    query: "test",
    properties: [{
        pid: "123",
        name: "Test Property",
        prefecture: "Tokyo",
        country: "JP",
        images: ["https://via.placeholder.com/400"],
        ts_stay_text: "Test description",
        likes_count: 10
    }]
});
```

---

## Integration with Existing Webhook

Your webhook server (`webhook_server.py`) already returns the correct data format:

```python
@app.route('/recommend', methods=['POST'])
def recommend_properties():
    # ... search logic ...

    return jsonify({
        "properties": [
            {
                "pid": str(ts['tsid']),
                "name": ts['name'],
                "prefecture": ts['prefecture'],
                "country": ts['country'],
                "images": ts.get('images', []),
                "stay_images": ts.get('stay_images', []),
                "ts_stay_text": ts.get('ts_stay_text', ''),
                "ts_text": ts.get('ts_text', ''),
                "likes_count": ts.get('likes_count', 0),
                # ... more fields
            }
            for ts in results
        ]
    })
```

**No changes needed** - webhook is already compatible!

---

## Next Steps

### Phase 1: Core Integration (Dec 24-26)

- [x] Create client tools implementation
- [x] Create production HTML page
- [ ] Update agent with client tools config
- [ ] Test voice + visual flow
- [ ] Deploy to Render.com

### Phase 2: Enhancements (Dec 27-30)

- [ ] Add calendar widget integration (showCalendar tool)
- [ ] Add booking flow (navigateToBooking tool)
- [ ] Improve mobile responsive design
- [ ] Add property image galleries
- [ ] Add filter UI (budget, dates, preferences)

### Phase 3: Polish (Dec 31 - Jan 1)

- [ ] Record demo Loom video
- [ ] Test with real users (Eric, Owen, Jeff)
- [ ] Optimize performance (lazy loading images)
- [ ] Add analytics (track property views, bookings)
- [ ] Final QA and bug fixes

---

## Demo Script for Jan 1st

**User**: [Clicks voice button]

**Kyoko**: "Hello! I'm Kyoko, your KABUK travel concierge. What kind of Japan experience are you looking for?"

**User**: "I want mountain hot springs with beautiful views, something relaxing"

**Kyoko**:
1. [Calls webhook to search]
2. [Calls showProperties - cards appear on screen]
3. "Perfect! I found 5 amazing mountain hot springs. Let me show you my top recommendations..."
4. [Calls highlightProperty on first property]
5. "This ryokan in Nagano has incredible mountain views and authentic outdoor baths..."
6. [Highlights second property]
7. "This one is perfect for a peaceful retreat with traditional kaiseki meals..."
8. "Would you like to see more details about any of these?"

**User**: "Tell me more about the first one"

**Kyoko**:
1. [Calls openPropertyDetail]
2. [Modal opens with full property details, gallery]
3. "This is Tsubakino Ryokan, located in the Japan Alps. It features..."

**Result**: User experiences seamless voice + visual journey

---

## Cost Implications

**Client Tools**: $0 additional cost
- Run in user's browser (client-side)
- No server overhead
- No API charges

**ElevenLabs Usage**: Same as voice-only
- ~$0.02 per conversation (unchanged)
- Client Tools don't add to voice/LLM costs

**Infrastructure**: Existing Render.com deployment
- Static HTML file (negligible)
- Same webhook server (already running)

**Total added cost**: $0 ✅

---

## File Locations

- **Production page**: `/static/kyoko-voice-demo.html`
- **Testing environment**: `/static/index-with-agent-testing.html`
- **Webhook server**: `webhook_server.py`
- **Setup guide**: `CLIENT_TOOLS_SETUP_GUIDE.md` (this file)
- **Original analysis**: `/tmp/client-tools-analysis.md`

---

## Support Resources

- **ElevenLabs Docs**: https://elevenlabs.io/docs/agents-platform
- **Client Tools Reference**: https://elevenlabs.io/docs/agents-platform/customization/tools/client-tools
- **Conversational AI SDK**: https://elevenlabs.io/docs/agents-platform/conversational-ai-sdk
- **KABUK Webhook API**: http://localhost:5001/ (see landing page)

---

**Status**: ✅ Implementation complete, ready for agent configuration
**Timeline**: Can be live today (Dec 24) if agent configured
**Blocker**: Need ElevenLabs agent ID and client tools setup in dashboard
