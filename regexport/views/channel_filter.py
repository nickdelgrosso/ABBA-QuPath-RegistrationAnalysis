from typing import Dict, List

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QWidgetItem, QLayout
from traitlets import HasTraits, List as TList, Instance, link, observe, directional_link

from regexport.model import AppState
from regexport.views.labelled_slider import LabelledSliderView, LabelledSliderModel
from regexport.views.utils import HasWidget


class ChannelFilterModel(HasTraits):
    sliders = TList(Instance(LabelledSliderModel))

    def register(self, model: AppState):
        self.model = model
        directional_link(
            (model, 'max_numspots_filters'),
            (self, 'sliders'),
            lambda max_filters: self.create_new_sliders(max_filters),
        )

    def create_new_sliders(self, max_numspots_filters: Dict[str, int]) -> List[LabelledSliderModel]:
        if set(slider.label for slider in self.sliders) != set(max_numspots_filters):
            sliders = []
            for chan, v in max_numspots_filters.items():
                slider = LabelledSliderModel(label=chan, max=v, value=v)
                slider.observe(self._update_model)
                sliders.append(slider)
            return sliders
        return self.sliders

    def _update_model(self, change):
        self.model.max_numspots_filters = {slider.label: slider.value for slider in self.sliders}



class ChannelFilterView(HasWidget):

    def __init__(self, model: ChannelFilterModel):
        self.model = model

        widget = QWidget()
        HasWidget.__init__(self, widget=widget)

        self.layout = QVBoxLayout()
        widget.setLayout(self.layout)

        self.model.observe(self.render)

    def render(self, change):

        if len(change.old) != len(change.new):
            layout: QLayout = self.layout

            # Delete any existing sliders
            if (num_sliders := layout.count()) > 0:
                for idx in reversed(range(num_sliders)):
                    item: QWidgetItem = layout.itemAt(idx)
                    layout.removeItem(item)
                    item.widget().deleteLater()

            layout.update()
            assert layout.count() == 0  # should be no sliders in the layout at this point.

            # Make new sliders
            for slider_model in change.new:
                print(f"making slider from {slider_model}")
                slider = LabelledSliderView(model=slider_model)
                layout.addWidget(slider.widget)
