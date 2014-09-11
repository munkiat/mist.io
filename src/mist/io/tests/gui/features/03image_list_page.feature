@image-list-page
Feature: Image List Page

  Background:
    # Wait 2 seconds before executing each step
    # mainly for headless testing performance issues
    When I wait for 2 seconds

  Scenario: Navigate to page by menu button
    When I visit mist.io
    And I click the button that contains "Images"
    Then the title should be "mist.io - images" within 10 seconds
    Then the header should be "Images" within 10 seconds

  Scenario: Navigate to page by url
    When I visit "/images"
    Then the title should be "mist.io - images" within 10 seconds
    Then the header should be "Images" within 10 seconds

  Scenario: Add backend for testing
    When I visit mist.io
    Given backends credentials
    Given "EC2 AP NORTHEAST" backend added

  Scenario: Filter images
    When I visit "/images"
    And I wait until images are loaded
    When I type "suse" into the images filter
    Then the first image should contain "suse"

  Scenario: Advaned Search - Star image
    When I visit "/images"
    And I type "django" into the images filter
    And I wait for 2 seconds
    And I click the button that contains "Continue search on server"
    And I wait until images are loaded
    Then the first image should contain "django"
    When I check the button that contains "django"
