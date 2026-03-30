Feature: User Login
  As a registered user
  I want to log into the application
  So that I can access my personalised dashboard

  Background:
    Given the application is running
    And the user is on the login page

  @smoke
  Scenario: Successful login with valid credentials
    When the user enters username "standard_user"
    And the user enters password "secret_sauce"
    And the user clicks the login button
    Then the user should be redirected to the dashboard
    And the welcome message "Welcome, Standard User" should be displayed

  @negative
  Scenario Outline: Login fails with invalid credentials
    When the user enters username "<username>"
    And the user enters password "<password>"
    And the user clicks the login button
    Then the error message "<error>" should be displayed
    And the user should remain on the login page

    Examples:
      | username      | password     | error                              |
      | invalid_user  | secret_sauce | Username and password do not match |
      | standard_user | wrong_pass   | Username and password do not match |
      |               | secret_sauce | Username is required               |
      | standard_user |              | Password is required               |

  @smoke
  Scenario: Successful logout after login
    Given the user is logged in as "standard_user"
    When the user clicks the logout button
    Then the user should be redirected to the login page
    And the session should be cleared

  @negative
  Scenario: Account locked after multiple failed attempts
    When the user enters username "locked_out_user"
    And the user enters password "secret_sauce"
    And the user clicks the login button
    Then the error message "Sorry, this user has been locked out" should be displayed

  @regression
  Scenario: Login page preserves username on failed attempt
    When the user enters username "standard_user"
    And the user enters password "wrong_password"
    And the user clicks the login button
    Then the username field should still contain "standard_user"
    And the password field should be cleared
