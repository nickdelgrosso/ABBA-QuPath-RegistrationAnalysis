from typing import List

from PyQt5.QtWidgets import QComboBox
from traitlets import HasTraits, List as TList, Unicode, directional_link, UseEnum, link

from model import AppState, AnalysisType
from views.utils import HasWidget


class AnalysisSelectorModel(HasTraits):
    analysis_type = UseEnum(AnalysisType, default_value=AnalysisType.RegionLabel)

    def register(self, model: AppState):
        link(
            (self, 'analysis_type'),
            (model, 'analysis_type')
        )


class AnalysisSelectorView(HasWidget):
    def __init__(self, model: AnalysisSelectorModel):
        self.dropdown = QComboBox()
        HasWidget.__init__(self, widget=self.dropdown)

        self.model = model
        self.set_dropdown_values(values=[analysis.name for analysis in self.model.analysis_type.__class__])
        self.model.observe(self.observe_analysis_type, ['analysis_type'])
        self.dropdown.currentTextChanged.connect(self.select_cmap_from_dropdown)

    def set_dropdown_values(self, values: List[str]):
        self.dropdown.clear()
        for value in values:
            self.dropdown.addItem(value)

    def observe_analysis_type(self, changed):
        self.dropdown.setCurrentText(self.model.analysis_type.name)

    def select_cmap_from_dropdown(self, text):
        print('selected', text)
        self.model.analysis_type = text