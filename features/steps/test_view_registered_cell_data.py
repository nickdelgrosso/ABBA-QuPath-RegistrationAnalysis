from dataclasses import dataclass, field, fields, Field
from pathlib import Path

from pytest import fixture
from pytest_bdd import when, then, given, scenario

from regexport.actions.load_atlas import LoadAtlasActionModel
from regexport.actions.load_cells import LoadCellsActionModel
from regexport.app import App
from regexport.model import AppState
from regexport.views.plot_3d import PlotterModel



@fixture()
def app() -> App:
    return App()


@scenario(
    '../view_registered_cell_data.feature',
    'Loading Data from TSV',
)
def test_data_shows_up_on_load():
    pass


@scenario(
    '../export_registered_data.feature',
    'Save Merged CSV',
)
def test_data_is_exported():
    pass

@given("the user has loaded the Allen Mouse Atlas")
def step_impl(app: App):
    app.load_atlas_button.click()


@given("no cells are plotted onscreeen")
def step_impl(app: App):
    plotted_points = app.plot_window.points
    assert len(plotted_points.coords) == 0  # no cells onscreen


@when("the user loads a TSV file exported from QuPath")
@given("the user has loaded a TSV file exported from QuPath")
def step_impl(app: App):
    app.load_cells_button.submit([
        Path("example_data/tsvs_exported_from_qupath/section1.tsv"),
        Path("example_data/tsvs_exported_from_qupath/section2.tsv"),
    ])

@then("the 3D cells positions should appear online")
def step_impl(app: App):
    plotted_points = app.plot_window.points
    assert plotted_points.coords.shape[1] == 3  # x, y, and z
    assert len(plotted_points.coords) > 500  # lots of cells onscreen loaded


@when("the user exports the data to file <export.csv>")
def step_impl(app: App):
    filename = Path("test_export.csv")
    app.export_data_button.submit(filename=filename)


@then("a single CSV file with is saved on the computer.")
def step_impl():
    filename = Path("test_export.csv")
    assert filename.exists()