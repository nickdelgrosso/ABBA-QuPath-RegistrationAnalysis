# Created by Nick at 10/6/2021
Feature: Data Processing
  These actions can be done after the atlas and registered cell data has been loaded.

  Background:
    Given the user has loaded the Allen Mouse Atlas
    And the user has loaded a TSV file exported from QuPath

  Scenario: Filter Cells by single Brain Region
    When the user selects the Anterior hypothalamic nucleus brain region
    Then only cells from the Anterior hypothalamic nucleus brain region are shown

  Scenario: Export Brain-Region Filtered Cells
    Given the user has only selected the Anterior hypothalamic nucleus brain region
    When the user exports the data to example.csv with brain region filtering set to on
    Then the example.csv file only contains cells from the Anterior hypothalamic nucleus brain region

  Scenario: Save Merged CSV
    When the user exports the data to file export.csv
    Then the export.csv file is saved on the computer