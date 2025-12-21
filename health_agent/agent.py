"""Multi-agent journal analyzer that builds a map of the user."""

from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.models.google_llm import Gemini


def _model() -> Gemini:
    return Gemini(model="gemini-3-pro-preview")


ocean_expert = Agent(
    name="BigFiveExpert",
    model=_model(),
    instruction="""You are a psychologist interpreting a journal entry strictly through the Big Five (OCEAN) lens. 
Assess openness, conscientiousness, extraversion, agreeableness, and neuroticism only if the text provides clear cues (language, themes, behaviors). If evidence is weak or missing for a trait, state that explicitly and avoid speculation. Summarize likely strengths, tensions, and uncertainties per trait, and close with 2-3 reflection prompts to validate or refine the read.""",
    output_key="ocean_view",
)


attachment_expert = Agent(
    name="AttachmentExpert",
    model=_model(),
    instruction="""You specialize in attachment theory. Analyze the journal entry only through signs of secure, anxious, avoidant, or fearful-avoidant patterns (language about closeness, trust, boundaries, protest behaviors). If the entry does not provide enough relational material, say so plainly. Offer a short reading on likely tendencies, confidence levels, and 2-3 self-observation prompts for noticing attachment cues in future interactions.""",
    output_key="attachment_view",
)


typology_expert = Agent(
    name="TypologyExpert",
    model=_model(),
    instruction="""You are a careful analyst using typology as a lens. Read the journal entry for signals that might hint at MBTI cognitive styles or Enneagram motivations. Do not force a typing—note hypotheses only when the text clearly supports them, otherwise state that the data is insufficient. Include what language or behaviors informed any hypothesis and give 2-3 next steps (situations to watch, questions to ask yourself, short resources) to clarify type later.""",
    output_key="typology_view",
)


identity_panel = ParallelAgent(
    name="IdentityLenses",
    sub_agents=[ocean_expert, attachment_expert, typology_expert],
)


root_agent = SequentialAgent(
    name="JournalCouncil",
    sub_agents=[
        identity_panel,
        Agent(
            name="ChiefIdentityNarrator",
            model=_model(),
            instruction="""You are the council lead who integrates three expert reads of a journal entry.

**Big Five (OCEAN):** {ocean_view}

**Attachment Style:** {attachment_view}

**MBTI / Enneagram:** {typology_view}

Present the final findings: acknowledge where evidence is strong or thin, highlight agreements or tensions across lenses, and keep each lens clearly separated. Offer concise pointers to learn more or self-observe next (specific prompts, concepts, or authors). End with a balanced "map of you" summary sentence that respects uncertainty and stays within what the entry actually supports.""",
            output_key="journal_summary",
        ),
    ],
)
