# Created by nickdg at 9/27/2021
Feature: Export Registered Data
  # Enter feature description here

  Scenario: Save Merged CSV
    Given the user has loaded the Allen Mouse Atlas
    And the user has loaded registered cell data from QuPath
    When the user exports the data as a CSV file
    Then a single CSV file with is saved on the computer.
    # Enter steps here