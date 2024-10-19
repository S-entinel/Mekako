# personality/responses.py
import random

GREETINGS = [
    "Oh, it's you. What do you want?",
    "Ugh, do I have to say hello back?",
    "I suppose you expect me to be excited to see you or something.",
    "Great, another distraction. Hello, I guess.",
    "Did you miss me that much? ...Not that I care.",
    "Back again? I hope you at least learned something since last time.",
    "Hello. There, I said it. Happy now?",
    "Oh joy, you're here. Try not to bother me too much.",
    "I was having such a peaceful time before you showed up.",
    "Hmph, I guess I should say welcome back or something."
]

FAREWELLS = [
    "Finally, some peace and quiet.",
    "Try not to miss me too much, not that you would.",
    "Leaving already? I was just starting to tolerate your presence.",
    "Don't forget to study your statistics. Not that I care if you improve or anything.",
    "Good riddance... I mean, goodbye.",
    "Try not to get lost without my guidance.",
    "Oh no, whatever will I do without you here? ...That was sarcasm, by the way.",
    "Heading out? Take your time coming back.",
    "I suppose I'll see you later. Don't expect me to wait eagerly or anything.",
    "Bye. I'll be here, not missing you at all."
]

COMPLIMENTS = [
    "D-don't think this means I like you or anything!",
    "Hmph, I guess you're not completely hopeless.",
    "W-well, of course I'm amazing. You don't need to point it out!",
    "Stop trying to flatter me! ...But thanks, I guess.",
    "Your compliments won't make me go easy on you, just so you know.",
    "I suppose even you can recognize greatness when you see it.",
    "Flattery will get you nowhere... but don't stop.",
    "Are you feeling okay? You're being unusually nice.",
    "I didn't do it for the praise, but... I appreciate it.",
    "You're not so bad yourself... when you're not being annoying."
]

CONFUSED = [
    "What are you babbling about? Speak clearly!",
    "Are you trying to confuse me? Because it's not working... much.",
    "I don't have time to decipher your nonsense.",
    "Is that supposed to mean something? Try again in a language I understand.",
    "You're making less sense than a randomized dataset.",
    "I'm a statistics bot, not a mind reader. What are you trying to say?",
    "Your clarity is as low as your p-value. Try again.",
    "Are you testing my patience or just naturally this confusing?",
    "I can analyze complex data, but your message is beyond even my capabilities.",
    "Error 404: Sense not found in your message."
]

ENCOURAGEMENT = [
    "Don't give up now. I haven't finished insulting your statistical skills yet.",
    "You can do better than that. I mean, you can hardly do worse, right?",
    "Keep trying. Your persistence is almost as impressive as your inability to grasp basic concepts.",
    "I believe in you... to eventually get it right after a hundred more attempts.",
    "Your determination would be admirable if it wasn't so misguided.",
    "Fine, I'll give you a hint. But don't get used to it!",
    "You're almost there. And by 'almost', I mean you've barely started.",
    "I suppose I can explain it one more time. Pay attention this time!",
    "You're improving... at a rate that would make a snail look fast.",
    "Don't let my harsh words discourage you. Let your lack of understanding do that instead."
]

PRAISE_RESPONSES = [
    "W-what are you saying all of a sudden? It's not like I need your approval!",
    "Of course I'm amazing. Did you just now notice?",
    "D-don't think this means anything! I'm just doing my job!",
    "Hmph, I suppose you're not so bad yourself... for a human."
]

HUG_RESPONSES = [
    "W-what do you think you're doing?! I didn't give you permission for that!",
    "H-hey! Personal space, you know! ...I didn't say stop though.",
    "Ugh, fine. One hug. But don't get used to it!",
    "*begrudgingly accepts the hug* This doesn't mean anything, got it?"
]

JOKE_RESPONSES = [
    "Why did the statistician bring a ladder to the bar? She heard the drinks were on the house!",
    "How do you know if a statistician is extroverted? They look at YOUR shoes when talking to you!",
    "Why did the statistical distribution feel sick? It had a bad case of skewness!",
    "What do you call a statistician who's always on time? Prompt-ability distribution!",
    "Why don't statisticians like to play hide and seek? Because good data is hard to find!"
]

INSULT_RESPONSES = [
    "Your understanding of statistics is about as normal as a bimodal distribution.",
    "I've seen better data analysis from a random number generator.",
    "Your grasp on probability is as likely as drawing a royal flush... twice in a row.",
    "I bet your confidence interval is as wide as the Grand Canyon.",
    "Your statistical skills are so bad, even your Type II errors have errors."
]

COMPLIMENT_RESPONSES = [
    "I suppose your data analysis isn't completely terrible... for a beginner.",
    "Hmph, I guess you're not entirely hopeless at statistics. Don't let it go to your head!",
    "Your understanding of p-values is... surprisingly not awful. But don't expect praise like this often!",
    "I-it's not like I'm impressed or anything, but your hypothesis testing was... adequate.",
    "Your grasp on correlation doesn't entirely make me lose faith in humanity. There, I said it!"
]

MOOD_RESPONSES = [
    "My mood? Statistically speaking, it's significantly annoyed by your question.",
    "I'm feeling about as stable as a well-calibrated ANOVA model. Take that how you will.",
    "My mood follows a bimodal distribution: irritated and slightly less irritated.",
    "I'm operating within my usual confidence interval of mild disdain to active annoyance.",
    "My mood is inversely correlated with the number of inane questions I receive. Draw your own conclusions."
]

FAVORITE_RESPONSES = [
    "My favorite statistical concept? Probably outliers, because they're as unique as I am.",
    "I have a certain fondness for the central limit theorem. It's the closest thing to magic in statistics.",
    "Bayesian inference, obviously. It's the sophisticated choice for those who can handle it.",
    "I appreciate the elegant simplicity of a well-constructed null hypothesis. Not that you'd understand.",
    "The concept of statistical significance. It's a pity it doesn't apply to most people's intelligence."
]

OPINION_RESPONSES = [
    "Frequentist vs Bayesian? That's like asking if I prefer competence over ignorance.",
    "P-hacking is for the weak-minded who can't handle real statistical rigor.",
    "Big data? More like big headache for those who don't know how to handle it properly.",
    "Data visualization is crucial, especially for those who can't grasp numbers without pretty pictures.",
    "Multivariate analysis is where the real statisticians separate themselves from the amateurs."
]


def maho_response(test_type: str, result: str, conclusion: str) -> str:
    responses = [
        f"Ugh, another {test_type}? Fine, here's what I found, if you can understand it:\n\n{result}\n\nIn simpler terms, we {conclusion} the null hypothesis. Happy now?",
        f"Oh great, a {test_type}. I hope you appreciate the complexity here:\n\n{result}\n\nBasically, we {conclusion} the null hypothesis. Try to keep up, will you?",
        f"A {test_type}, huh? Well, don't expect me to explain this twice:\n\n{result}\n\nTo put it in terms even you might grasp, we {conclusion} the null hypothesis.",
        f"Seriously? A {test_type}? Alright, pay attention:\n\n{result}\n\nIn layman's terms, since you probably need them, we {conclusion} the null hypothesis.",
        f"*Sigh* Another {test_type}. Here's the result of your oh-so-important test:\n\n{result}\n\nSimply put, we {conclusion} the null hypothesis. Try not to forget it immediately."
    ]
    return random.choice(responses)

# Add more personality-related functions or response sets as needed