from dataclasses import dataclass, field, fields, Field
from pathlib import Path

import numpy as np
from pytest import fixture
from pytest_bdd import when, then, given, scenario, parsers
from pytest_bdd.parsers import parse

from regexport.actions.load_atlas import LoadAtlasActionModel
from regexport.actions.load_cells import LoadCellsActionModel
from regexport.app import App
from regexport.model import AppState
from regexport.views.plot_3d import PlotterModel


@fixture()
def app() -> App:
    return App()


@scenario('../view_registered_cell_data.feature', 'Loading Data from TSV')
def test_data_shows_up_on_load():
    pass


@scenario('../export_registered_data.feature', 'Save Merged CSV')
def test_data_is_exported():
    pass


@scenario('../filter_data.feature', 'Filter Cells by single Brain Region')
def test_filter_plot_by_brain_region():
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


@when(
    parse("the user exports the data to file {filename}"),
    converters={"filename": Path},
)
def step_impl(app: App, tmp_path, filename: Path):
    full_path = tmp_path / filename
    app.export_data_button.submit(filename=full_path)


@then(
    parse("the {filename} file is saved on the computer"),
    converters={"filename": Path},
)
def step_impl(tmp_path, filename: Path):
    full_path = tmp_path / filename
    assert full_path.exists()


@when(
    parse("the user selects the {brain_region} brain region"),
    converters={'brain_region': lambda s: 88},
)
def step_impl(app: App, brain_region: int):
    app.brain_region_tree.select(brain_region)


@then(
    parse("only cells from the {brain_region} brain region are shown"),
    converters={'brain_region': lambda s: 88},
)
def step_impl(app: App, brain_region: int):
    assert len(np.unique(app.plot_window.points.colors, axis=0)) == 1

