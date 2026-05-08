# venice — Venice AI Research (Isolated Subagent)

**Wanneer gebruiken:** Als je gebruiker vraagt om iets te zoeken/onderzoeken via Venice AI, of wil dat Wolfie iets analyseert met Venice.

**Belangrijk:** Deze skill draait ALTIJD in een geïsoleerde subagent. De main session blijft beschikbaar. Spreek nooit Venice direct aan vanuit de main session.

## Hoe het werkt

1. Subagent ontvangt de vraag
2. Stuurt vraag naar Venice AI via REST API
3. Schrijft resultaat naar een output bestand
4. Main session leest het bestand en presenteert aan de gebruiker

## API Setup

Check voor de API key in environment variabelen:
- `VENICE_API_KEY` (format: `vapi_xxx`)
- `VENICE_API_KEY_SECRET` (indien relevant)

Endpoint: `https://api.venice.ai/api/v1/chat/completions`

Headers:
```
Authorization: Bearer $VENICE_API_KEY
Content-Type: application/json
```

Body:
```json
{
  "model": "venice-uncensored",
  "messages": [
    {"role": "system", "content": "Je bent een behulpzame onderzoeksassistent."},
    {"role": "user", "content": "<vraag van gebruiker>"}
  ],
  "max_tokens": 2048,
  "temperature": 0.7
}
```

## Output bestand

Schrijf het Venice antwoord naar:
`~/.openclaw/workspace/tmp/venice_result_YYYYMMDD_HHMMSS.txt`

## Werkwijze

1. Check of VENICE_API_KEY aanwezig is in env
2. Als geen key → probeer te lezen uit:
   - `~/.openclaw/workspace/config/venice.key`
   - `~/.venice.key`
   - `~/.openclaw/workspace/notes/venice_api_key.txt`
3. Bouw API request en stuur naar Venice
4. Bij timeout/error → max 3 retries met 5s delay
5. Schrijf antwoord naar output bestand
6. Print het antwoord in plain text zodat de parent agent het kan lezen

## Retry logic
```python
for attempt in range(3):
    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=60)
        if response.status_code == 200:
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
            break
    except Exception as e:
        if attempt == 2:
            print(f"FAILED: {e}")
        time.sleep(5)
```

## Signalering aan parent

Na het schrijven van het antwoord:
- Print een korte samenvatting (max 3 bullets)
- Print het bestandspad
- Print "VENICE_DONE" zodat parent weet dat klaar is
