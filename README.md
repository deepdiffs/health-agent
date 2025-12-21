# Journal Analyzer Agent

Multi-agent council that reads a raw journal entry to surface who you are through three psychological lenses: Big Five/OCEAN, attachment styles, and MBTI/Enneagram hypotheses. Each expert stays in its lane, avoids speculation when evidence is thin, and the council narrator delivers a balanced "map of you."

## Agents
- `BigFiveExpert`: looks only for OCEAN trait signals and notes gaps when unclear.
- `AttachmentExpert`: checks for secure/anxious/avoidant/fearful-avoidant patterns; says if relational cues are missing.
- `TypologyExpert`: cautious MBTI/Enneagram hints with evidence; refuses to force a type.
- `JournalCouncil`: runs the three in parallel (`IdentityLenses`) and produces the final synthesis.

## Quick start
1. Set `GOOGLE_API_KEY` for Gemini access.
2. Install deps: `pip install -e .`.
3. Run with your journal text:

```bash
python - <<'PY'
import asyncio
from google.adk.runners import InMemoryRunner
from health_agent.agent import root_agent

journal_text = """I noticed..."""
runner = InMemoryRunner(agent=root_agent)
response = asyncio.run(runner.run_debug(journal_text))
print(response)
PY
```
