# Created by nickdg at 9/27/2021
Feature: Filter Registered Data
  # Enter feature description here

  Scenario: Filter Cells by single Brain Region
    Given the user has loaded the Allen Mouse Atlas
    And the user has loaded a TSV file exported from QuPath
    When the user selects the Anterior hypothalamic nucleus brain region
    Then only cells from the Anterior hypothalamic nucleus brain region are shown

    