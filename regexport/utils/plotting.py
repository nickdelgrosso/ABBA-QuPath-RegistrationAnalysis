import numpy as np
from matplotlib.colors import ListedColormap


def convert_values_to_colors(color_codes: np.ndarray, cmap: ListedColormap):
    return cmap(color_codes / color_codes.max())[:, :4]
