import pandas as pd
from bg_atlasapi import BrainGlobeAtlas


def read_detection_file(filename: str, atlas: BrainGlobeAtlas) -> pd.DataFrame:
    df = pd.read_csv(filename, sep='\t')
    print(df.columns)
    return (
        df
        .rename(columns={'Allen CCFv3 X mm': 'X', 'Allen CCFv3 Y mm': 'Y', 'Allen CCFv3 Z mm': 'Z'})
        .astype({'X': float, 'Y': float, 'Z': float})
        .pipe(lambda df: df.assign(
            BGIdx=atlas.annotation[
                (df.X / (atlas.resolution[0] / 1000)).values.astype(int),
                (df.Y / (atlas.resolution[1] / 1000)).values.astype(int),
                (df.Z / (atlas.resolution[2] / 1000)).values.astype(int),
            ]
        ))
        .merge(atlas.lookup_df, right_on="id", left_on="BGIdx", how="left")
        .astype({'acronym': 'category', 'name': 'category'})
        .drop(columns=['id'])
    )#.sample(10000)