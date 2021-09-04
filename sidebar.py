from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPushButton
from bg_atlasapi import BrainGlobeAtlas

from model import AppState, read_detection_file
from utils import HasWidget


class Sidebar(HasWidget):

    def __init__(self, model: AppState):
        self.model = model

        widget = QWidget()
        HasWidget.__init__(self, widget=widget)

        layout = QVBoxLayout()
        widget.setLayout(layout)

        button = QPushButton('Load TSVs')
        layout.addWidget(button)
        button.clicked.connect(self.load_data)

    def load_data(self):
        print('loading data')
        df = read_detection_file(
            filename='D:/QuPath Projects/Project3/export2/PW166-A14_Scan1_[4314,45057]_component_data_merged_Region 2.ome.tif__detections2.tsv',
            atlas=self.model.atlas, )
        print('data loaded')
        print('assigning data')
        self.model.cells = df
        print('data assigned')




