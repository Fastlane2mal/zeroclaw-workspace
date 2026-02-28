Infrastructure
- OpenRouter auto router selected as primary LLM provider for ZeroClaw.
- Groq and Gemini incompatible with ZeroClaw tool calling — both output raw tool syntax instead of executing.
- OpenRouter free tier with tool calling support confirmed working.
- Fallback chain: openrouter/auto → groq → gemini.
