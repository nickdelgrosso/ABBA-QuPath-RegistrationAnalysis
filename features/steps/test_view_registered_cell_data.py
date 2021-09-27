from dataclasses import dataclass, field, fields, Field
from pathlib import Path

from pytest import fixture
from pytest_bdd import when, then, given, scenario

from regexport.actions.load_atlas import LoadAtlasActionModel
from regexport.actions.load_cells import LoadCellsActionModel
from regexport.model import AppState
from regexport.views.plot_3d import PlotterModel


@dataclass
class AppWidgets:
    load_atlas_button: LoadAtlasActionModel = field(default_factory=LoadAtlasActionModel)
    load_cells_button: LoadCellsActionModel = field(default_factory=LoadCellsActionModel)
    plot_window: PlotterModel = field(default_factory=PlotterModel)

    def __post_init__(self):
        self.model = AppState()
        for field in fields(self):
            field: Field
            viewmodel = getattr(self, field.name)
            viewmodel.register(model=self.model)


@fixture()
def app() -> AppWidgets:
    return AppWidgets()


@scenario(
    '../view_registered_cell_data.feature',
    'Loading Data from TSV',
)
def test_data_shows_up_on_load():
    pass


@given("the user has loaded the Allen Mouse Atlas")
def step_impl(app: AppWidgets):
    app.load_atlas_button.click()


@given("no cells are plotted onscreeen")
def step_impl(app: AppWidgets):
    plotted_points = app.plot_window.points
    assert len(plotted_points.coords) == 0  # no cells onscreen


@when("the user loads a TSV file exported from QuPath")
def step_impl(app: AppWidgets):
    app.load_cells_button.submit([
        Path("example_data/tsvs_exported_from_qupath/section1.tsv"),
        Path("example_data/tsvs_exported_from_qupath/section2.tsv"),
    ])


@then("the 3D cells positions should appear online")
def step_impl(app: AppWidgets):
    plotted_points = app.plot_window.points
    assert plotted_points.coords.shape[1] == 3  # x, y, and z
    assert len(plotted_points.coords) > 500  # lots of cells onscreen loaded
