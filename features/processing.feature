# Created by Nick at 10/6/2021
Feature: Data Processing
  These actions can be done after the atlas and registered cell data has been loaded.

  Background:
    Given the user has loaded the Allen Mouse Atlas
    And the user has loaded a TSV file exported from QuPath

  Scenario: Filter Cells by single Brain Region
    When the user selects the Anterior hypothalamic nucleus brain region
    Then only cells from the Anterior hypothalamic nucleus brain region are shown

  Scenario: Filter Cells by Number of Spots in a Specific Channel
    When the user sets the maximum number of spots in the Esr1 (Opal 480) channel to 50
    Then only cells that have up to 50 spots in the Esr1 (Opal 480) channel are shown
    And the proportion of cells rejected by the Esr1 (Opal 480) channel setting is shown to be somewhere between 0% and 100%

  Scenario: Visualize Distribution of Number of Spots in a Specific Channel
    When the user sets the maximum number of spots in the Esr1 (Opal 480) channel to 50
    And the user sets the visualization to the Esr1 (Opal 480) channel
    Then a histogram is shown with the number of spots distribution from 0 to 50 spots

  Scenario: Export Brain-Region Filtered Cells
    Given the user has only selected the Anterior hypothalamic nucleus brain region
    When the user exports the data to example.csv with export visible cells set to on
    Then the example.csv file only contains cells from the Anterior hypothalamic nucleus brain region

  Scenario: Export Receptor-Filtered Cells
    Given the user sets the maximum number of spots in the Esr1 (Opal 480) channel to 30
    When the user exports the data to example.csv with export visible cells set to on
    Then the example.csv file only contains cells that have 30 or less spots from the Esr1 (Opal 480) channel

  Scenario: Export Brain-Region and Receptor-Filtered Cells
    Given the user has only selected the Anterior hypothalamic nucleus brain region
    And the user sets the maximum number of spots in the Esr1 (Opal 480) channel to 30
    When the user exports the data to example.csv with export visible cells set to on
    Then the example.csv file only contains cells that have 30 or less spots from the Esr1 (Opal 480) channel
    Then the example.csv file only contains cells from the Anterior hypothalamic nucleus brain region

  Scenario: Save Merged CSV
    When the user exports the data to file export.csv
    Then the export.csv file is saved on the computer
