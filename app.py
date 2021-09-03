import sys

import pandas as pd
from PyQt5.QtWidgets import QApplication

from bg_atlasapi import BrainGlobeAtlas

from ui import MainWindow, PlotterWindow, BrainRegionTree


def read_detection_file(filename: str, atlas: BrainGlobeAtlas) -> pd.DataFrame:
    return (
        pd.read_csv(filename, sep='\t')
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
    ).sample(10000)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow(
        main_widgets=[
            BrainRegionTree(),
            PlotterWindow(
                cells=read_detection_file(
                    filename='D:/QuPath Projects/Project3/export2/PW166-A14_Scan1_[4314,45057]_component_data_merged_Region 2.ome.tif__detections2.tsv',
                    atlas=(atlas := BrainGlobeAtlas("allen_mouse_25um")),
                ),
                atlas=atlas,
            ),
        ]
    )
    win.show()
    sys.exit(app.exec_())
