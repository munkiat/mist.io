@key-list-page
Feature: Key List Page

  Background:
    # Wait 2 seconds before executing each step
    # mainly for headless testing performance issues
    When I wait for 2 seconds

  Scenario: Navigate to page by menu button
    When I visit mist.io
    And I click the button that contains "Keys"
    Then the title should be "mist.io - keys" within 10 seconds
    Then the header should be "Keys" within 10 seconds

  Scenario: Navigate to page by url
    When I visit "/keys"
    Then the title should be "mist.io - keys" within 10 seconds
    Then the header should be "Keys" within 10 seconds

  Scenario: Add key
    When I visit "/keys"
    And I click the "Add" button
    And I type "Bacon" in key name input
    And I click the "Generate" button inside the "Add key" popup
    And I wait until private key is filled
    And I click the "Add" button inside the "Add key" popup
    Then "Bacon" key should be added within 15 seconds

  Scenario: Rename key
    When I visit "/keys"
    And I check the button that contains "Bacon"
    And I click the "Rename" button
    And I type "Eggs" in new key name input
    And I click the "Save" button inside the "Rename key" popup
    Then "Eggs" key should be added within 15 seconds

  Scenario: Delete key
    When I visit "/keys"
    And I check the button that contains "Eggs"
    And I click the "Delete" button
    And I click the "Yes" button
    Then "Eggs" key should be removed

  Scenario: Set default keys
    Given a key named "Foo"
    Given a key named "Bar"
    When I check the button that contains "Foo"
    And I click the "Set default" button
    Then "Foo" should be the default key
    When I check the button that contains "Foo"
    And I check the button that contains "Bar"
    And I click the "Set default" button
    Then "Bar" should be the default key

  Scenario: Filter keys
    When I visit "/keys"
    When I type "Foo" into the keys filter
    Then "Bar" key should be removed
    When I type "Bar" into the keys filter
    Then "Foo" key should be removed
    When I type "Bacon" into the keys filter
    Then "Foo" key should be removed
    And "Bar" key should be removed

  Scenario: Clean up
    When I visit "/keys"
    When I delete all keys
