# Created by nickdg at 9/27/2021
Feature: Export Registered Data
  # Enter feature description here

  Scenario: Save Merged CSV
    Given the user has loaded the Allen Mouse Atlas
    And the user has loaded a TSV file exported from QuPath
    When the user exports the data to file export.csv
    Then the export.csv file is saved on the computer
    # Enter steps here