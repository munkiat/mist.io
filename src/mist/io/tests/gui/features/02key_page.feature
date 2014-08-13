@key-page
Feature: Single Key Page

  Background:
    # Wait 2 seconds before executing each step
    # mainly for headless testing performance issues
    When I wait for 2 seconds

  Scenario: Add a key for testing
    Given a key named "Bacon"

  Scenario: Navigate to page by buttons
    When I visit mist.io
    And I click the button that contains "Keys"
    And I click the button that contains "Bacon"
    Then the title should be "mist.io - Bacon" within 10 seconds
    Then the header should be "Bacon" within 10 seconds

  Scenario: Navigate to page by url
    When I visit "/keys/Bacon"
    Then the title should be "mist.io - Bacon" within 10 seconds
    Then the header should be "Bacon" within 10 seconds

  Scenario: View public and private keys
    When I visit "/keys/Bacon"
    Then I should see the public key
    When I click the button that contains "Private key"
    And I click the "Display" button
    Then I should see the private key

  Scenario: Rename key
    When I visit "/keys/Bacon"
    And I click the "Rename" button
    And I type "Eggs" in new key name input
    And I click the "Save" button inside the "Rename key" popup
    Then the header should be "Eggs" within 10 seconds

  Scenario: Delete key
    When I visit "/keys/Eggs"
    And I click the "Delete" button
    And I click the "Yes" button
    Then the title should be "mist.io - keys" within 10 seconds
    And the header should be "Keys" within 10 seconds
    And "Eggs" key should be removed
