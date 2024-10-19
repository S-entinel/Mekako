# utils/intents.py
import re
import random
from ..personality.responses import GREETINGS, FAREWELLS, COMPLIMENTS, ENCOURAGEMENT

class Intent:
    def __init__(self, name, patterns, responses):
        self.name = name
        self.patterns = patterns
        self.responses = responses

    def get_response(self, message):
        if self.name == "stats_term":
            term = re.search(self.patterns[0], message, re.IGNORECASE).group()
            return random.choice(self.responses).format(term=term)
        return random.choice(self.responses)

intents = [
    Intent("greeting", 
           [r'\b(hi|hello|hey|greetings)\b'],
           GREETINGS),
    Intent("farewell", 
           [r'\b(bye|goodbye|see\s+you|farewell)\b'],
           FAREWELLS),
    Intent("gratitude", 
           [r'\b(thanks|thank\s+you|appreciate)\b'],
           [
               "Hmph, it's not like I did it for you or anything.",
               "You're welcome, I guess. Don't expect special treatment next time.",
               "Of course you're grateful. My help is invaluable.",
               "Thanks? Well... you're not completely useless either.",
               "I suppose your gratitude is... not entirely unwelcome."
           ]),
    Intent("compliment", 
           [r'\b(good|great|awesome|amazing|excellent|brilliant)\b'],
           COMPLIMENTS),
    Intent("question", 
           [r'\?'],
           [
               "Do I look like a search engine to you?",
               "Have you tried figuring it out yourself first?",
               "That's your question? Really?",
               "Ugh, fine. I'll help, but only because your confusion is painful to watch.",
               "I suppose I can enlighten you. Pay attention, I won't repeat myself."
           ]),
    Intent("help", 
           [r'\b(help|confused|don\'t\s+understand|explain)\b'],
           ENCOURAGEMENT),
    Intent("stats_term", 
           [r'\b(mean|median|mode|variance|standard\s+deviation|probability|hypothesis|correlation|regression|anova|t-test|chi-square)\b'],
           [
               "Oh, so you're interested in {term}? I'm surprised you even know what that is.",
               "Ah, {term}. A concept that's probably way over your head, but I can try to explain.",
               "{term}? Well, at least you're asking about something worthwhile for once.",
               "Hmph, I suppose I could enlighten you about {term}. Try to keep up.",
               "You want to know about {term}? Fine, but pay attention. I won't explain it twice."
           ]),
    # Add more intents as needed
]

def get_intent(message):
    for intent in intents:
        if any(re.search(pattern, message, re.IGNORECASE) for pattern in intent.patterns):
            return intent
    return None