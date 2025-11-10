Feature: login_success Testing
  @login_success
  Scenario: Test login_success functionality
    Given User navigates to 'https://map.chronicle.rip/'
    When User clicks 'Login'
    Then 'Login to your account' should be visible
    When User enters 'faris+astanaorg@chronicle.rip' in the Email box
    And User enters '12345' in the Password box
    And User clicks 'LOGIN'
    Then User navigates to 'https://aus.chronicle.rip/customer-organization/Astana_Tegal_Gundul'
    Then 'Astana Tegal Gundul' should be visible
    And 'Private' should be visible