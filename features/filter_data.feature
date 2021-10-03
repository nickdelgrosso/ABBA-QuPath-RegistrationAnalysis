# Created by nickdg at 9/27/2021
Feature: Filter Registered Data
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