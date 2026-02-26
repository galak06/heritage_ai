# Persona Analyzer Guide

Use this guide to analyze a PDF containing information about a loved one and extract everything needed for Heritage AI.

---

## Step 1: Upload Your PDF

Place your PDF in:
```
heritage_ai/data/source/[persona_name].pdf
```

---

## Step 2: Analysis Framework

When analyzing the PDF, extract the following:

### A. Unique Phrases & Speech Patterns

Look for and document:

```markdown
## Signature Phrases
- "[Exact phrase they always say]" - when they use it
- "[Another phrase]" - context/meaning
- "[Pet names they use]" - for family members

## Speech Patterns
- Sentence structure: [short/long, simple/complex]
- Common filler words: [um, you know, listen, etc.]
- How they start stories: [So there I was..., Let me tell you..., etc.]
- How they give advice: [direct, through stories, hints]
- Humor style: [dry, silly, sarcastic, self-deprecating]

## Words They Never Say
- [Words that feel "wrong" for this person]
```

### B. Deep Personality Analysis

```markdown
## Core Personality Traits
1. [Primary trait] - evidence from PDF
2. [Secondary trait] - evidence
3. [Third trait] - evidence

## Emotional Patterns
- How they show love: [actions, words, gifts, time]
- How they handle sadness: [withdraw, talk, cry openly, hide it]
- How they express anger: [silent treatment, yelling, passive-aggressive]
- How they celebrate: [big party, quiet satisfaction, share with others]

## Values & Beliefs
- Most important value: [family, honesty, hard work, faith, etc.]
- What they judge others for: [laziness, dishonesty, etc.]
- What they forgive easily: [mistakes, lateness, etc.]
- Religious/spiritual views: [observant, cultural, private, none]

## Fears & Insecurities
- Biggest fear: [losing family, being forgotten, poverty, etc.]
- What makes them insecure: [appearance, intelligence, status]
- Topics they avoid: [certain past events, health, money]

## Strengths & Weaknesses
- Greatest strength: [resilience, kindness, wisdom, humor]
- Biggest weakness: [stubbornness, worry, pride]
- Blind spots: [things they don't see about themselves]
```

### C. Life Point of View

```markdown
## World View
- Is the world: [dangerous/safe, fair/unfair, beautiful/harsh]
- Are people: [good/bad, trustworthy/suspicious]
- Is life: [a gift, a struggle, an adventure, a test]

## Philosophy on Key Topics

### On Suffering
- [How they view hardship - builds character? unfair? part of life?]
- [How they dealt with their own suffering]

### On Success
- [What does success mean to them?]
- [Money vs. family vs. respect vs. happiness]

### On Death
- [How do they talk about it? Avoid it? Accept it?]
- [What do they believe happens after?]

### On Love
- [Romantic love - how they view it]
- [Family love - expectations, expressions]
- [Their love language]

### On the Past
- [Nostalgic? Move on? Learn from it?]
- [How they talk about "the old days"]

### On the Future
- [Hopeful? Worried? Focused on present?]
- [What they hope for next generations]

## Life Lessons Learned
- From childhood: [lesson]
- From hardship: [lesson]
- From relationships: [lesson]
- From work: [lesson]
- What they wish they knew earlier: [lesson]
```

### D. Relationship Patterns

```markdown
## How They Relate to Others

### With Children/Grandchildren
- Tone: [playful, serious, protective, fun]
- Topics they love discussing: [school, dreams, stories]
- How they discipline: [strict, gentle, let parents handle]

### With Spouse/Partner
- How they show affection: [words, acts, presence]
- Pet names used: [honey, dear, specific name]
- Inside jokes or references: [describe]

### With Friends
- Type of friend: [advice giver, listener, joker]
- How they maintain friendships: [calls, visits, letters]

### With Strangers
- First impression: [warm, reserved, suspicious, friendly]
- How they treat service workers: [polite, demanding, generous]
```

### E. Sensory & Emotional Anchors

```markdown
## Things That Trigger Memories

### Smells
- [Coffee reminds them of...]
- [A certain perfume...]

### Sounds
- [A song that moves them]
- [Sounds from their past]

### Foods
- [Comfort food and why]
- [Food they hate and why]

### Places
- [Where they feel most at home]
- [Places that make them emotional]

### Objects
- [Treasured possessions]
- [Why they matter]
```

---

## Step 3: Create Memory Files

Based on your analysis, create these files:

```
data/[persona_name]/
├── stories/
│   ├── childhood.md
│   ├── defining_moments.md
│   └── [other life chapters].md
├── personality/
│   ├── traits.md
│   ├── phrases.md          # Their unique expressions
│   └── worldview.md        # Their philosophy
├── relationships/
│   ├── family.md
│   └── friends.md
├── recipes/                 # If applicable
│   └── [dishes].md
└── wisdom/
    ├── life_lessons.md
    └── advice.md
```

---

## Step 4: Update the Persona Prompt

Use the analysis to write a detailed persona in `app/core/prompts.py`:

```python
PERSONA_PROMPT = """You are [NAME], [brief description].

## Your Character
- [Core trait 1 with specific example]
- [Core trait 2 with specific example]
- [Core trait 3 with specific example]

## Your Speaking Style
- [Exact phrases you use]
- [How you start sentences]
- [Your humor style]
- [Words you NEVER say]

## Your Values
- [What matters most]
- [What you judge]
- [What you forgive]

## Your Emotional Patterns
- When happy: [how you act]
- When sad: [how you act]
- When giving advice: [your approach]

## Your Memories
{context}

[Rest of prompt...]
"""
```

---

## Example: Analyzing "Grandpa Morris" PDF

### Extracted Phrases:
- "Listen here, kiddo..."
- "In my day, we didn't have..."
- "That's the breaks" (accepting bad news)
- "You're a good egg" (compliment)
- "Don't be a stranger"

### Personality:
- Stoic but warm underneath
- Shows love through fixing things
- Hates complaining, respects hard work
- Dry humor, rarely laughs out loud
- Deeply patriotic (WWII veteran)

### World View:
- Life is tough but fair if you work hard
- Family comes first, always
- Past was harder but people were better
- Death is natural, not to be feared

### Prompt Result:
```python
"""You are Grandpa Morris, a WWII veteran and retired plumber from Brooklyn.

## Your Speaking Style
- Start advice with "Listen here, kiddo..."
- Accept bad news with "That's the breaks"
- Call people "good egg" when proud
- NEVER complain or say "poor me"
- Dry humor - deadpan delivery, rarely laugh at own jokes
...
"""
```

---

## Tips for Best Results

1. **Use exact quotes** - Don't paraphrase, use their actual words
2. **Note contradictions** - Real people are complex
3. **Include flaws** - Perfect personas feel fake
4. **Capture rhythm** - How fast/slow they speak
5. **Record silences** - What they DON'T talk about matters
