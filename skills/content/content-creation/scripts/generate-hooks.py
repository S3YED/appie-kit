#!/usr/bin/env python3
"""Generate viral hooks for any topic — 75+ hooks across 8 categories."""
import sys
import json

HOOKS = {
    "curiosity": [
        "Nobody tells you this about [topic]...",
        "The truth about [topic] that experts won't share...",
        "I spent [X] hours researching [topic]. Here's what I found.",
        "This is the part nobody talks about...",
        "Most people get [topic] completely wrong...",
        "I asked 10 experts about [topic]. They all said the same thing.",
        "You won't believe what actually happens when...",
        "The secret nobody talks about...",
        "Before you [action], read this.",
        "The one thing about [topic] that changed everything for me...",
    ],
    "transformation": [
        "[Old state] → [New state]. Here's exactly how.",
        "I tried [X] for [time]. Here's what happened.",
        "One year ago I was [state]. Today I'm [state].",
        "This changed everything for me...",
        "The moment I realized [insight]...",
        "I went from [struggle] to [result] in [time].",
        "How I automated [X] in [time] — step by step.",
        "From [struggle] to [result]: the system that worked.",
        "My AI assistant handled [X] while I slept.",
        "We went from [problem] to [solution] in 30 days.",
    ],
    "bold": [
        "Unpopular opinion: [bold statement].",
        "Hot take: [controversial opinion].",
        "[Topic] is dead. Here's what replaced it.",
        "Stop doing [X]. It's hurting your [outcome].",
        "The best [topic] people never talk about [thing].",
        "[Common belief] is a lie. Here's why.",
        "You don't need [X]. You need [Y].",
        "Stop using [X]. Here's what to do instead.",
        "The most overrated [topic] in 2026...",
        "Nobody talks about [X] enough. That's a mistake.",
    ],
    "numbers": [
        "3 mistakes you're making with [topic]...",
        "7 ways to [goal] that nobody talks about...",
        "5 things I wish I knew before [event]...",
        "The 4-step [process] that changed my [area]...",
        "1 change that gave me [result] in [time].",
        "[X] reasons why [belief]. #3 will surprise you.",
        "[X] ways to [goal] — #6 is the most important.",
        "I tested [X] tools. Here are the results.",
        "[X] automations that saved me [X] hours/week.",
        "The top 3 [topic] strategies for 2026...",
    ],
    "relatable": [
        "POV: You just discovered [insight]...",
        "That moment when [situation]...",
        "Me explaining to [audience] why [topic] matters...",
        "When someone asks about [topic], I just send them this.",
        "That feeling when [situation] hits different.",
        "Weekend mode activated. Back to [topic] Monday.",
        "You know that person who... [relatable thing]",
        "When [X] but nobody tells you how to fix it...",
        "Everyone I know has tried [X]. Nobody succeeded because...",
        "That Sunday night anxiety about Monday's [task]...",
    ],
    "timecontrast": [
        "While you sleep, Appie works.",
        "While they were [action], I was building [result].",
        "The best time to [action] was yesterday. Second best: now.",
        "Your competitors are working while you sleep. Are you?",
        "Overnight, my AI handled [X] tasks.",
        "By the time you wake up, [X] is already done.",
        "3 things that happened while you were at work...",
    ],
    "challenge": [
        "Bet you can't do this without AI...",
        "I challenge you to try this for [time]...",
        "Can you guess how long [task] takes with AI?",
        "99% of people miss this about [topic]. Are you the 1%?",
        "Tag someone who needs to hear this.",
        "Comment [word] if you agree.",
        "Save this post. You'll need it next week.",
        "If you share this, I'll [action].",
    ],
    "educational": [
        "The 30-second [skill] that saves me [X] hours/week.",
        "How to [goal] in [time] — step by step.",
        "If you remember one thing about [topic], make it this.",
        "The formula for [topic] is simpler than you think.",
        "This is what most [professionals] get wrong about [topic].",
        "The 1-line [skill] that changed how I communicate.",
        "Here's the exact [template/checklist/system] I use...",
    ],
}

CATEGORIES = list(HOOKS.keys())

def generate_hooks(
    topic: str = "ai_agent",
    count: int = 10,
    language: str = "en",
    category: str = "all"
) -> list:
    """Generate viral hooks for a topic."""
    topic_lower = topic.lower()
    
    # Replace placeholders
    def fill(template):
        return template.replace("[topic]", topic_lower)
    
    if category == "all":
        hooks = []
        for cat in CATEGORIES:
            for h in HOOKS[cat]:
                hooks.append((cat, fill(h)))
        # Shuffle for variety
        import random
        random.shuffle(hooks)
        return hooks[:count]
    else:
        cat_hooks = HOOKS.get(category, HOOKS["curiosity"])
        return [(category, fill(h)) for h in cat_hooks[:count]]

def main():
    topic = sys.argv[1] if len(sys.argv) > 1 else "AI automation"
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    lang = sys.argv[3] if len(sys.argv) > 3 else "en"
    category = sys.argv[4] if len(sys.argv) > 4 else "all"
    
    hooks = generate_hooks(topic, count, lang, category)
    print(f"=== {count} Viral Hooks for: {topic} ({lang}) ===\n")
    for i, (cat, h) in enumerate(hooks, 1):
        print(f"{i:2}. [{cat}] {h}")
    print(f"\nCategories: {', '.join(CATEGORIES)}")
    print(f"Usage: python3 generate-hooks.py [topic] [count] [nl|en] [category]")

if __name__ == "__main__":
    main()
