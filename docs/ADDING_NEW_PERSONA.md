# Adding a New Persona to Heritage AI

This guide walks you through preserving a new loved one's memories.

## Quick Start (5 steps)

### Step 1: Copy the Template
```bash
cp -r templates/persona_template data/
# Rename to your person's name
mv data/persona_template data/grandpa_joe
```

### Step 2: Fill In Their Stories
Edit the markdown files in your new folder:
- `stories/childhood.md` - Where they grew up, family, school
- `stories/life_journey.md` - Career, marriage, raising family
- `recipes/favorite_dish.md` - Their signature recipes
- `wisdom/life_lessons.md` - Advice and favorite sayings
- `wisdom/favorite_things.md` - Music, hobbies, interests

**Tips for gathering memories:**
- Record conversations with them (or family members who remember)
- Look through old photos - they trigger stories
- Ask specific questions: "What was your first job?" not "Tell me about yourself"
- Write in THEIR voice, as if they're telling the story

### Step 3: Update the Persona Prompt
Edit `app/core/prompts.py`:

1. Open `templates/persona_template/PERSONA_PROMPT.md` for examples
2. Replace the character description with your person
3. Capture their speaking style - how do they actually talk?

### Step 4: Point to the New Data Folder
Edit `app/core/config.py`:
```python
data_path: Path = Path("data/grandpa_joe")  # Change this
```

Or set environment variable:
```bash
export DATA_PATH=data/grandpa_joe
```

### Step 5: Ingest and Test
```bash
# Restart the server
# Then ingest the new memories
curl -X POST http://localhost:8000/ingest

# Test it
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about yourself"}'
```

---

## Detailed Guide

### Gathering Memories

The quality of the AI depends on the quality of the memories you capture.

**Best sources:**
1. **Direct interviews** - Sit down with them, ask questions, record audio
2. **Family members** - Siblings, children who have stories
3. **Letters/journals** - Written in their own words
4. **Photo albums** - Go through together, write down what they say
5. **Home videos** - Transcribe meaningful moments

**Good questions to ask:**
- "What's your earliest memory?"
- "How did you and [spouse] meet?"
- "What was your favorite thing about [parent]?"
- "What's the hardest thing you ever went through?"
- "What advice would you give your younger self?"
- "What's your secret to [their specialty - cooking, fixing things, etc.]?"

### Writing in Their Voice

Don't write ABOUT them. Write AS them.

**Bad:**
> My grandmother made chicken soup every Friday.

**Good:**
> Every Friday, I'd start the soup early morning. The smell would fill the whole house by the time the kids came home from school.

### Organizing Memories

Create categories that fit THEIR life:

| Person Type | Suggested Categories |
|-------------|---------------------|
| Grandparent | stories, recipes, wisdom, family |
| Veteran | stories, military, wisdom, hobbies |
| Artist | stories, art, inspiration, techniques |
| Immigrant | homeland, journey, new_life, traditions |

### Testing Your Persona

After ingesting, test with these prompts:
```bash
# Identity
"Who are you?"
"Tell me about your childhood"

# Specific memories (should find context)
"How did you meet grandma?"
"What's your chicken soup recipe?"

# Off-topic (should be warm but honest)
"What do you think about TikTok?"
"Should I buy Bitcoin?"
```

---

## Multiple Personas

To support multiple people in one instance:

1. Keep each person's data in separate folders:
   ```
   data/
   ├── savta/
   ├── grandpa_joe/
   └── nonna_rosa/
   ```

2. Create separate ChromaDB collections (modify config)

3. Add a `persona` parameter to the chat endpoint (requires code changes)

---

## Tips for Authenticity

1. **Imperfection is real** - Include their quirks, repeated stories, strong opinions
2. **Specific > Generic** - "The blue house on Maple Street" beats "where I grew up"
3. **Emotions matter** - How did they FEEL, not just what happened
4. **Their words** - Use their actual phrases, not polished writing
5. **Gaps are okay** - Real people don't remember everything

---

## Need Help?

- Check `templates/persona_template/` for file templates
- See `data/` (Savta) for a working example
- API docs at http://localhost:8000/docs
