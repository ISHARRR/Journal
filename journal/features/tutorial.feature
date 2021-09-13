Feature: showing off behave

  Scenario: Search for an account
    Given I search for a valid account
    Then I will see the account details
