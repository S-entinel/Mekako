# utils/plotting.py
import matplotlib.pyplot as plt
import seaborn as sns
import io
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

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

def plot_distribution(dist_func, params, x_range, title):
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

def save_plot_as_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return buf

# Add more plotting functions as needed