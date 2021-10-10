from pathlib import Path
from typing import Tuple, List

import numpy as np
import pandas as pd
from bg_atlasapi import BrainGlobeAtlas


def read_detection_file(filename: Path, atlas: BrainGlobeAtlas) -> pd.DataFrame:
    df = pd.read_csv(filename, sep='\t')
    print(df.columns)
    x_mm_col = 'Allen CCFv3 X mm'
    y_mm_col = 'Allen CCFv3 Y mm'
    z_mm_col = 'Allen CCFv3 Z mm'
    return (
        df
            .astype({
                x_mm_col: float,
                y_mm_col: float,
                z_mm_col: float,
        })
            .pipe(lambda df: df.assign(
                BGIdx=get_brain_region_label(df[x_mm_col].values, df[y_mm_col].values,
                                             df[z_mm_col].values, annotation=atlas.annotation,
                                             resolution=atlas.resolution)))
            .merge(atlas.lookup_df, right_on="id", left_on="BGIdx", how="left")
            .rename(columns={
                x_mm_col: 'X',
                y_mm_col: 'Y',
                z_mm_col: 'Z',
                'name': 'BrainRegion',
                'acronym': 'Acronym',
        })
            .drop(columns=['id'])
            .assign(Image=filename.name)
    )  # .sample(10000)


def get_brain_region_label(x, y, z, annotation: np.ndarray, resolution: Tuple[int, int, int]) -> np.ndarray:
    sx, sy, sz = annotation.shape
    rx, ry, rz = resolution
    return annotation[
        np.clip((x / (rx / 1000)).astype(int), 0, sx - 1),
        np.clip((y / (ry / 1000)).astype(int), 0, sy - 1),
        np.clip((z / (rz / 1000)).astype(int), 0, sz - 1),
    ]


def read_detection_files(filenames: List[Path], atlas):
    df = pd.concat((read_detection_file(filename=filename, atlas=atlas) for filename in filenames), ignore_index=True)
    df = df.astype({'Acronym': 'category', 'BrainRegion': 'category', 'Image': 'category'})
    return df
