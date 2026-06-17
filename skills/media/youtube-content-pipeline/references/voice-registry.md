# YouTube Channel Voice Registry

## Official Channel Voices

| Channel | Voice ID | Provider | Purpose | Status |
|---------|----------|----------|---------|--------|
| Global Signal | `auq43ws1oslv0tO4BDa7` | ElevenLabs | Brian voice for all geopolitics/finance videos | LOCKED - NEVER CHANGE |

## Voice Assignment Rules

1. **Global Signal YouTube Channel**: ALWAYS use `auq43ws1oslv0tO4BDa7`
2. **Scalaro Marketing**: Use professional male voice (default Brian if not specified)
3. **Amaan Academy**: Use warm, educational voice (specify per project)

## Changing Voices

To update a voice assignment:
1. Edit this registry
2. Update all scripts referencing the old voice ID
3. Test with a short sample before full production
4. Document reason for change in git commit

## Voice Testing Checklist

Before using any voice in production:
- [ ] Generate 30-second test sample
- [ ] Check pronunciation of key terms (geopolitics, country names)
- [ ] Verify pacing matches video length (150 WPM target)
- [ ] Confirm tone matches channel brand (authoritative for Global Signal)
- [ ] Test with background music at -20db

## API Key Validation

Before production runs, validate API keys:

### ElevenLabs
```bash
curl -s -X GET "https://api.elevenlabs.io/v1/voices" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" | head -20
```
- **200 OK**: Key valid, voices listed
- **401 Unauthorized**: Key invalid or expired. Get new key at https://elevenlabs.io/settings/api-keys
- **No output**: Check network/DNS

### Test Voice Generation
```bash
curl -s -X POST "https://api.elevenlabs.io/v1/text-to-speech/auq43ws1oslv0tO4BDa7" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text":"Welcome to Global Signal","model_id":"eleven_monolingual_v1"}' \
  -o /tmp/test.mp3
```
- Check `/tmp/test.mp3` exists and has size > 0
- If empty: Voice ID may be wrong or key lacks credits

## Troubleshooting Voice Issues

### HTTP 401 Unauthorized
- **Cause**: Invalid API key
- **Fix**: Generate new key at https://elevenlabs.io/settings/api-keys
- **Prevention**: Validate key before batch jobs

### HTTP 422 Unprocessable Entity
- **Cause**: Voice ID not found or model mismatch
- **Fix**: Verify voice ID in ElevenLabs Voice Library
- **Check**: `curl -H "xi-api-key: $KEY" https://api.elevenlabs.io/v1/voices | grep auq43ws1oslv0tO4BDa7`

### Slow Generation / Timeouts
- **Cause**: Large scripts or API overload
- **Fix**: Chunk scripts to <5000 chars per request
- **Fix**: Add retry with exponential backoff

### Credits Exhausted
- **Cause**: Free tier limit reached
- **Fix**: Upgrade plan or add credits at https://elevenlabs.io/pricing
- **Check**: `curl -H "xi-api-key: $KEY" https://api.elevenlabs.io/v1/user/subscription`
