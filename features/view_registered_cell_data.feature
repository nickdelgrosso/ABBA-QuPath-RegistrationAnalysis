# Created by nickdg at 9/27/2021
Feature:
  Visualize registered cell positions in 3D

  Scenario: Loading Data from TSV
    Given the user has loaded the Allen Mouse Atlas
    Given no cells are plotted onscreeen
    When the user loads a TSV file exported from QuPath
    Then the 3D cells positions should appear online


