
Feature: All Features
  # Enter feature description here

  Scenario: Export Qupath Cell-Registration Groovy Script
    When the user requests the QuPath TSV cell export script to file script.groovy
    Then the script.groovy file is saved on the computer

  Scenario: Loading Data from TSV
    Given the user has loaded the Allen Mouse Atlas
    Given no cells are plotted onscreen
    When the user loads a TSV file exported from QuPath
    Then the 3D cells positions should appear online

  Scenario: Download Useful ABBA-QuPath Plugin Files
    When the user asks that ABBA Plugin files be downloaded to the ABBA_plugins directory
    Then the ABBA_plugins directory contains many ABBA files



