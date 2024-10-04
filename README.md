# Mekako
Mekako is a Discord bot is designed to assist with advanced statistical analysis, with its own unique personality

## Features

- **Comprehensive Statistical Functions**: Includes z-tests, t-tests, ANOVA, chi-square tests, correlation analyses, regression, and more.
- **Probability Distributions**: Supports normal, exponential, gamma, beta, uniform, t, F, and chi-squared distributions.
- **Combinatorics**: Calculates factorials, combinations, and permutations.
- **Data Visualization**: Generates beautiful, 3Blue1Brown-inspired plots for various statistical analyses.
- **LaTeX Rendering**: Renders LaTeX equations for mathematical expressions.
- **Simulations**: Includes coin flip and dice roll simulations.
- **Unique Personality**: Responds with a tsundere attitude, making interactions both informative and entertaining.

## Commands

Here's a list of some key commands:

- `!ztest`: Perform a z-test
- `!ttest`: Perform a t-test
- `!anova`: Perform one-way ANOVA
- `!chisquare`: Perform chi-square goodness of fit test
- `!correlation`: Calculate Pearson correlation
- `!regression`: Perform simple linear regression
- `!normal`: Calculate normal distribution probability density
- `!binomial`: Calculate binomial probability
- `!poisson`: Calculate Poisson probability
- `!factorial`: Calculate factorial
- `!combination`: Calculate combinations
- `!histogram`: Create a histogram
- `!boxplot`: Create a box plot
- `!latex`: Render a LaTeX equation

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/S-entinel/mekako-bot.git
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your Discord bot token:
   ```
   DISCORD_TOKEN=your_token_here
   ```

4. Run the bot:
   ```
   python main.py
   ```

## Dependencies

- discord.py
- numpy
- scipy
- matplotlib
- seaborn
- python-dotenv


## Acknowledgments

- Inspired by Maho Hiyajo from Steins;Gate
- Plotting style inspired by 3Blue1Brown

## Disclaimer

This bot has a tsundere personality and may occasionally respond with snarky or dismissive comments. It's all in good fun and not meant to offend. Use at your own risk!
