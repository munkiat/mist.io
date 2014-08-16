@image-list-page
Feature: Image List Page

  Background:
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

  @wip
  Scenario: Add backend for testing
    When I visit mist.io
    Given backends credentials
    Given "EC2 AP NORTHEAST" backend added

  Scenario: Filter images
    When I visit "/images"
    And I wait until images are loaded
    When I type "suse" into the images filter
    Then the first image should contain "suse"

  @wip
  Scenario: Advaned Search - Star image
    When I visit "/images"
    And I type "django" into the images filter
    And I click the button that contains "Continue search on server"
    And I wait until images are loaded
    Then the first image should contain "django"
    When I check the button that contains "django"


#  Scenario: Unstar image
#
#
#
#    When I search for a "django" Image
#    And I click the button that contains "Continue search on server"
#    Then Images list should be loaded within 60 seconds
#
#    When I star an Image that contains "django"
#    And I clear the Images search bar
#    Then Images list should be loaded within 30 seconds
#    And an Image that contains "django" should be starred
#
#    @web
#    Scenario: Star Image
#        When I click the "Add backend" button
#        And I click the "Select provider" button
#        And i click the "EC2 AP Sydney" button
#        And I use my "EC2" credentials
#        And I click the "Add" button
#        And I wait for 1 seconds
#            Then I should see the "EC2 AP Sydney" Backend added within 30 seconds#
#
#        When I click the "Images" button
#        And I wait for 3 seconds
#        And I star a "SUSE" image
#        And I visit mist.io
#        And I click the "Images" button
#        And I wait for 5 seconds
#            Then the first/second image should be "SUSE"
#
#
#    @web
#    Scenario: Advance Search - Star Image
#        When I click the "Images" button
#        And I type "django" in images search box
#        And I click the "Continue search on server..." button
#            Then I should see "django" images within 50 seconds
#        When I star a "django" image
#        And I visit mist.io
#        And I click the "Images" button
#        And I wait for 5 seconds
#           Then the first/second image should be "django"
#
