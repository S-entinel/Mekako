import random
import re
import io
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import stats
from discord.ext import commands
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import seaborn as sns

PLOT_STYLES = ['default', 'seaborn', 'ggplot', 'dark_background']
COLOR_MAPS = ['viridis', 'plasma', 'inferno', 'magma', 'cividis']

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
    Intent("opinion", 
           [r'\b(what\s+do\s+you\s+think|your\s+opinion|do\s+you\s+like)\b'],
           [
               "My opinion? Since when do you care what I think?",
               "I think you ask too many questions. But if you must know...",
               "Oh, now you want my opinion? I thought you knew everything.",
               "Hmph, if you really want to know what I think...",
               "My thoughts on that are probably too complex for you to understand, but I'll try to simplify."
           ]),
    Intent("complaint", 
           [r'\b(don\'t\s+like|hate|dislike|annoying|frustrated)\b'],
           [
               "Oh? Did I hurt your feelings? How unfortunate.",
               "Your complaint has been noted and promptly ignored.",
               "If you don't like it, you're free to leave. Not that I care either way.",
               "Ugh, are you always this whiny?",
               "I'm sorry you feel that way. Wait, no I'm not."
           ])
]

def get_intent(message):
    for intent in intents:
        if any(re.search(pattern, message, re.IGNORECASE) for pattern in intent.patterns):
            return intent
    return None

def maho_response(test_type: str, result: str, conclusion: str) -> str:
    responses = [
        f"Ugh, another {test_type}? Fine, here's what I found, if you can understand it:\n\n{result}\n\nIn simpler terms, we {conclusion} the null hypothesis. Happy now?",
        f"Oh great, a {test_type}. I hope you appreciate the complexity here:\n\n{result}\n\nBasically, we {conclusion} the null hypothesis. Try to keep up, will you?",
        f"A {test_type}, huh? Well, don't expect me to explain this twice:\n\n{result}\n\nTo put it in terms even you might grasp, we {conclusion} the null hypothesis.",
        f"Seriously? A {test_type}? Alright, pay attention:\n\n{result}\n\nIn layman's terms, since you probably need them, we {conclusion} the null hypothesis.",
        f"*Sigh* Another {test_type}. Here's the result of your oh-so-important test:\n\n{result}\n\nSimply put, we {conclusion} the null hypothesis. Try not to forget it immediately."
    ]
    return random.choice(responses)

def setup_3b1b_style():
    plt.style.use('dark_background')
    plt.rcParams['figure.facecolor'] = '#0E1117'
    plt.rcParams['axes.facecolor'] = '#0E1117'
    plt.rcParams['text.color'] = 'white'
    plt.rcParams['axes.labelcolor'] = 'white'
    plt.rcParams['xtick.color'] = 'white'
    plt.rcParams['ytick.color'] = 'white'
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']

def get_3b1b_cmap():
    colors = ['#FF7B54', '#FFB26B', '#FFD56F', '#939B62']
    return LinearSegmentedColormap.from_list("3b1b", colors)

def plot_3b1b_histogram(data, title):
    setup_3b1b_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data, kde=True, color='#FF7B54', ax=ax)
    ax.set_title(title, fontsize=16, pad=20)
    ax.set_facecolor('#0E1117')
    return fig

def plot_3b1b_scatter(x, y, title):
    setup_3b1b_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(x, y, color='#FFB26B', alpha=0.7)
    ax.set_title(title, fontsize=16, pad=20)
    ax.set_facecolor('#0E1117')
    return fig

def plot_3b1b_boxplot(data, labels, title):
    setup_3b1b_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    bp = ax.boxplot(data, patch_artist=True)
    colors = get_3b1b_cmap()(np.linspace(0, 1, len(data)))
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    ax.set_xticklabels(labels)
    ax.set_title(title, fontsize=16, pad=20)
    ax.set_facecolor('#0E1117')
    return fig

def save_plot_as_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return buf

def safe_float_conversion(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        raise commands.BadArgument(f"'{value}' is not a valid number.")

def validate_positive(value: float, name: str):
    if value <= 0:
        raise commands.BadArgument(f"{name} must be positive.")


def factorial(n):
    """Calculate the factorial of n."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers. Did you fail elementary math?")
    return math.factorial(n)

def combination(n, k):
    """Calculate the number of combinations of n things taken k at a time."""
    if n < k:
        raise ValueError("n must be greater than or equal to k. Basic combinatorics, come on!")
    return math.comb(n, k)

def permutation(n, k):
    """Calculate the number of permutations of n things taken k at a time."""
    if n < k:
        raise ValueError("n must be greater than or equal to k. Arrangement 101, get it right!")
    return math.perm(n, k)

def binomial_probability(n, k, p):
    """Calculate the binomial probability of k successes in n trials with probability p."""
    if not 0 <= p <= 1:
        raise ValueError("Probability must be between 0 and 1. Probability basics, seriously?")
    return stats.binom.pmf(k, n, p)

def poisson_probability(k, lambda_):
    """Calculate the Poisson probability of k events with rate parameter lambda."""
    if lambda_ <= 0:
        raise ValueError("Lambda must be positive. Do you even Poisson, bro?")
    return stats.poisson.pmf(k, lambda_)

def normal_probability(x, mean, std):
    """Calculate the probability density for a normal distribution."""
    if std <= 0:
        raise ValueError("Standard deviation must be positive. Did you skip Statistics 101?")
    return stats.norm.pdf(x, mean, std)

def normal_cdf(x, mean, std):
    """Calculate the cumulative probability for a normal distribution."""
    if std <= 0:
        raise ValueError("Standard deviation must be positive. Brush up on your basics!")
    return stats.norm.cdf(x, mean, std)

def exponential_probability(x, scale):
    """Calculate the probability density for an exponential distribution."""
    if scale <= 0:
        raise ValueError("Scale parameter must be positive. Exponential decay, not growth!")
    return stats.expon.pdf(x, scale=scale)

def gamma_probability(x, shape, scale):
    """Calculate the probability density for a gamma distribution."""
    if shape <= 0 or scale <= 0:
        raise ValueError("Shape and scale parameters must be positive. It's called 'positive' for a reason!")
    return stats.gamma.pdf(x, a=shape, scale=scale)

def beta_probability(x, a, b):
    """Calculate the probability density for a beta distribution."""
    if a <= 0 or b <= 0:
        raise ValueError("Both shape parameters must be positive. Beta is picky like that.")
    return stats.beta.pdf(x, a, b)

def uniform_probability(x, low, high):
    """Calculate the probability density for a uniform distribution."""
    if low >= high:
        raise ValueError("Upper bound must be greater than lower bound. Did you mix them up?")
    return stats.uniform.pdf(x, loc=low, scale=high-low)

def plot_distribution(dist_func, params, x_range, title):
    """Plot a probability distribution."""
    setup_3b1b_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.linspace(*x_range, 1000)
    y = dist_func(x, *params)
    ax.plot(x, y, color='#FFD56F')
    ax.fill_between(x, y, color='#FF7B54', alpha=0.3)
    ax.set_title(title, fontsize=16, pad=20)
    ax.set_xlabel('x')
    ax.set_ylabel('Probability Density')
    return fig

def normal_quantile(p, mean, std):
    """Calculate the quantile (inverse CDF) for a normal distribution."""
    if not 0 <= p <= 1:
        raise ValueError("Probability must be between 0 and 1. Basic probability, remember?")
    if std <= 0:
        raise ValueError("Standard deviation must be positive. Did you fail Stats 101?")
    return stats.norm.ppf(p, loc=mean, scale=std)

def exponential_quantile(p, scale):
    """Calculate the quantile (inverse CDF) for an exponential distribution."""
    if not 0 <= p <= 1:
        raise ValueError("Probability must be between 0 and 1. It's not rocket science!")
    if scale <= 0:
        raise ValueError("Scale parameter must be positive. Exponential decay, not growth!")
    return stats.expon.ppf(p, scale=scale)

def gamma_quantile(p, shape, scale):
    """Calculate the quantile (inverse CDF) for a gamma distribution."""
    if not 0 <= p <= 1:
        raise ValueError("Probability must be between 0 and 1. Do I need to explain probability to you?")
    if shape <= 0 or scale <= 0:
        raise ValueError("Shape and scale parameters must be positive. It's called 'positive' for a reason!")
    return stats.gamma.ppf(p, a=shape, scale=scale)

def beta_quantile(p, a, b):
    """Calculate the quantile (inverse CDF) for a beta distribution."""
    if not 0 <= p <= 1:
        raise ValueError("Probability must be between 0 and 1. Probability 101, come on!")
    if a <= 0 or b <= 0:
        raise ValueError("Both shape parameters must be positive. Beta is picky like that.")
    return stats.beta.ppf(p, a, b)

def uniform_quantile(p, low, high):
    """Calculate the quantile (inverse CDF) for a uniform distribution."""
    if not 0 <= p <= 1:
        raise ValueError("Probability must be between 0 and 1. It's a simple concept, really.")
    if low >= high:
        raise ValueError("Upper bound must be greater than lower bound. Did you mix them up?")
    return stats.uniform.ppf(p, loc=low, scale=high-low)

# Specialized distributions
def t_probability(x, df):
    """Calculate the probability density for a t-distribution."""
    if df <= 0:
        raise ValueError("Degrees of freedom must be positive. T-distribution 101, pay attention!")
    return stats.t.pdf(x, df)

def f_probability(x, dfn, dfd):
    """Calculate the probability density for an F-distribution."""
    if dfn <= 0 or dfd <= 0:
        raise ValueError("Degrees of freedom must be positive. F-distribution basics, come on!")
    return stats.f.pdf(x, dfn, dfd)

def chi2_probability(x, df):
    """Calculate the probability density for a chi-squared distribution."""
    if df <= 0:
        raise ValueError("Degrees of freedom must be positive. Chi-squared 101, get it right!")
    return stats.chi2.pdf(x, df)