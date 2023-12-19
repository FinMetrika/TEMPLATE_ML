import matplotlib.pyplot as plt
import numpy as np

def get_n_colors(n, cmap_name='viridis'):
    """
    Generate a list of n discrete colors using a Matplotlib colormap.

    :param n: Number of discrete colors
    :param cmap_name: Name of the colormap to use
    :return: List of n colors
    """
    cmap = plt.cm.get_cmap(cmap_name, n)  # Get the colormap
    colors = cmap(np.linspace(0, 1, n))   # Generate colors
    
    return colors