from pathlib import Path

import numpy as np
import pandas as pd
from pytest import fixture
from pytest_bdd import when, then, given, scenario
from pytest_bdd.parsers import parse

from regexport.app import App


@fixture()
def app() -> App:
    return App()


@scenario('view_registered_cell_data.feature', 'Loading Data from TSV')
def test_data_shows_up_on_load():
    pass


@scenario('export_registered_data.feature', 'Save Merged CSV')
def test_data_is_exported():
    pass


@scenario('filter_data.feature', 'Filter Cells by single Brain Region')
def test_filter_plot_by_brain_region():
    pass


@scenario('filter_data.feature', 'Export Brain-Region Filtered Cells')
def test_exported_data_is_filtered_by_brain_region():
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
@given(
    parse("the user has only selected the {brain_region} brain region"),
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


@when(
    parse("the user exports the data to {filename} with brain region filtering set to {is_brain_region_filter}"),
    converters={
        'filename': Path,
        'is_brain_region_filter': lambda s: {'on': True, 'off': False},
    }
)
def step_impl(app: App, tmp_path, filename: Path, is_brain_region_filter: bool):
    full_filename = tmp_path / filename
    app.export_data_button.submit(filename=full_filename, selected_regions_only=is_brain_region_filter)


@then(
    parse("the {filename} file only contains cells from the {brain_region} brain region"),
    converters={'filename': Path},
)
def step_impl(tmp_path, filename, brain_region):
    full_filename = tmp_path / filename
    df = pd.read_csv(full_filename)
    brain_regions_in_file = df.BrainRegion.unique()
    assert len(brain_regions_in_file) == 1
    assert brain_regions_in_file[0] == brain_region
