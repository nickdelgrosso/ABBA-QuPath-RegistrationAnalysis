from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap


@dataclass(frozen=True)
class PointCloud:
    coords: np.ndarray = field(default=np.empty((0, 3), dtype=float))
    colors: np.ndarray = field(default=np.empty((0, 3), dtype=float))
    alphas: np.ndarray = field(default=np.empty((0, 1), dtype=float))

    def __post_init__(self):
        assert self.coords.ndim == 2 and self.coords.shape[1] == 3
        assert self.colors.ndim == 2 and self.colors.shape[1] == 3
        assert self.alphas.ndim == 2 and self.alphas.shape[1] == 1


    @classmethod
    def from_cmap(cls, positions: np.ndarray, color_levels: np.ndarray, cmap: str = 'tab20c') -> PointCloud:
        selected_colors = convert_values_to_colors(color_levels, getattr(plt.cm, cmap))
        return cls(
            coords=positions,
            colors=selected_colors[:, :3],
            alphas=selected_colors[:, 3:4],
        )


def convert_values_to_colors(color_codes: np.ndarray, cmap: ListedColormap):
    return cmap(color_codes / color_codes.max())[:, :4]
