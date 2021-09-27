# Created by nickdg at 9/27/2021
Feature: Filter Registered Data
  # Enter feature description here

  Scenario: Filter Cells by single Brain Region
    Given the user has loaded the Allen Mouse Atlas
    And the user has loaded registered cell data from QuPath
    When the user selects the MPO brain region
    Then only cells from the MPO brain region are shown

    