
Feature: All Features
  # Enter feature description here

  Scenario: Filter Cells by single Brain Region
    Given the user has loaded the Allen Mouse Atlas
    And the user has loaded a TSV file exported from QuPath
    When the user selects the Anterior hypothalamic nucleus brain region
    Then only cells from the Anterior hypothalamic nucleus brain region are shown

  Scenario: Export Brain-Region Filtered Cells
    Given the user has loaded the Allen Mouse Atlas
    And the user has loaded a TSV file exported from QuPath
    And the user has only selected the Anterior hypothalamic nucleus brain region
    When the user exports the data to example.csv with brain region filtering set to on
    Then the example.csv file only contains cells from the Anterior hypothalamic nucleus brain region

  Scenario: Loading Data from TSV
    Given the user has loaded the Allen Mouse Atlas
    Given no cells are plotted onscreen
    When the user loads a TSV file exported from QuPath
    Then the 3D cells positions should appear online

  Scenario: Save Merged CSV
    Given the user has loaded the Allen Mouse Atlas
    And the user has loaded a TSV file exported from QuPath
    When the user exports the data to file export.csv
    Then the export.csv file is saved on the computer
