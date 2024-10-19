# commands/__init__.py
from .basic_stats import basic_stats_setup
from .distributions import distributions_setup
from .hypothesis_tests import hypothesis_tests_setup
from .visualizations import visualizations_setup
from .probability import probability_setup

def setup_commands(bot):
    basic_stats_setup(bot)
    distributions_setup(bot)
    hypothesis_tests_setup(bot)
    visualizations_setup(bot)
    probability_setup(bot)