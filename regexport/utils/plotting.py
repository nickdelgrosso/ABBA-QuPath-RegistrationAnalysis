from dataclasses import dataclass, field
from typing import Tuple

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap

from regexport.utils.profiling import warn_if_slow


@dataclass(frozen=True)
class PointCloud:
    coords: np.ndarray = field(default=np.empty((0, 3), dtype=float))
    colors: np.ndarray = field(default=np.empty((0, 3), dtype=float))
    alphas: np.ndarray = field(default=np.empty((0, 1), dtype=float))

    def __post_init__(self):
        assert self.coords.ndim == 2 and self.coords.shape[1] == 3
        assert self.colors.ndim == 2 and self.colors.shape[1] == 3
        assert self.alphas.ndim == 2 and self.alphas.shape[1] == 1


@warn_if_slow()
def plot_cells(positions: np.ndarray, colors: np.ndarray, indices: Tuple[int], cmap: str = 'tab20c') -> PointCloud:
    return PointCloud(
        coords=positions[indices, :],
        colors=(selected_colors := convert_values_to_colors(colors, getattr(plt.cm, cmap))[indices])[:, :3],
        alphas=selected_colors[:, 3:4],
    )


def convert_values_to_colors(color_codes: np.ndarray, cmap: ListedColormap):
    return cmap(color_codes / color_codes.max())[:, :4]