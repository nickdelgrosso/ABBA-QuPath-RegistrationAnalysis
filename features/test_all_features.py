from pathlib import Path

import numpy as np
import pandas as pd
from pytest import fixture
from pytest_bdd import when, then, given, scenarios
from pytest_bdd.parsers import parse

from regexport.app import App

scenarios('.')  # bind all scenarios in the current folder to pytest test functions


@fixture()
def app() -> App:
    return App()


@given("the user has loaded the Allen Mouse Atlas")
def step_impl(app: App):
    app.load_atlas_button.click()


@given("no cells are plotted onscreen")
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
    parse("the user exports the data to {filename} with export visible cells set to {export_visible_cells}"),
    converters={
        'filename': Path,
        'export_visible_cells': lambda s: {'on': True, 'off': False},
    }
)
def step_impl(app: App, tmp_path, filename: Path, export_visible_cells: bool):
    full_filename = tmp_path / filename
    app.export_data_button.submit(filename=full_filename, export_visible_cells_only=export_visible_cells)


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


@when(
    parse("the user requests the QuPath TSV cell export script to file {filename}"),
    converters={'filename': Path},
)
def step_impl(app: App, tmp_path, filename: Path):
    app.save_groovy_script_button.submit(tmp_path / filename)


@given(
    parse("the user sets the maximum {measurement} in the {channel_name} channel to {max_spots}"),
    converters={
        'max_spots': int,
        'measurement': lambda s: {"number of spots": "Num Spots"}[s]
    },
)
@when(
    parse("the user sets the maximum {measurement} in the {channel_name} channel to {max_spots}"),
    converters={
        'max_spots': int,
        'measurement': lambda s: {"number of spots": "Num Spots"}[s]
    },
)
def step_impl(app: App, measurement: str, channel_name: str, max_spots: int):
    full_channel_name = f"{channel_name}: {measurement}"
    app.channel_filter_model.set_max(full_channel_name, max_spots)


@then(
    parse("only cells that have up to {max_spots} spots in the {channel_name} channel are shown"),
    converters={'max_spots': int},
)
def step_impl(app: App, max_spots: int, channel_name: str):
    full_channel_name = f"{channel_name}: Num Spots"
    assert app.model.selected_cells[full_channel_name].max() <= max_spots


@when(
    parse("the user sets the visualization to the {channel_name} channel"),
)
def step_impl(app: App, channel_name: str):
    full_channel_name = f"{channel_name}: Num Spots"
    app.colordata_selector_dropdown.select(full_channel_name)


@then(
    parse("a histogram is shown with the number of spots distribution from {range_min} to {range_max} spots"),
    converters={'range_min': int, 'range_max': int},
)
def step_impl(app: App, range_min: int, range_max: int):
    hist = app.hist_plots
    assert max(hist.selected_data) == range_max
    assert min(hist.selected_data) == range_min


@then(
    parse("the proportion of cells rejected by the {channel_name} channel setting is shown to be {rejection_level}"),
    converters={'rejection_level': lambda val: None},  # haven't hard-coded the dataset, so can't predict value here.
)
def step_impl(app: App, channel_name: str, rejection_level):
    ...


@when(
    parse("the user asks that ABBA Plugin files be downloaded to the {directory} directory"),
    converters={'directory': Path},
)
def step_impl(app: App, tmp_path: Path, directory: Path):
    app.download_biop_extensions_button.submit(tmp_path / directory)


@then(
    parse("the {directory} directory contains many ABBA files"),
    converters={'directory': Path},
)
def step_impl(app: App, tmp_path: Path, directory: Path):
    assert (tmp_path / directory / "extensions").exists()


@then(
    parse(
        "the {filename} file only contains cells that have {max_spots} or less spots from the {channel_name} channel"),
    converters={
        'filename': Path,
        'max_spots': int,
    },
)
def step_impl(tmp_path: Path, filename: Path, max_spots: int, channel_name: str):
    df = pd.read_csv(tmp_path / filename)
    assert df[f"{channel_name}: Num Spots"].max() <= max_spots
