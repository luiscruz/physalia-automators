Feature: Physalia UI Interactions

  Scenario: Tap on views
    When I tap <view> for 10 times
    | view    |
    | button_1  |
    | button_2  |
    | button_3  |
    | fab       |

  Scenario: Long tap on views
    When I long tap <view> for 10 times
    | view    |
    | button_1  |
    | button_2  |
    | button_3  |
    | fab       |

  Scenario: Dragndrop
    When I dragndrop <first_view> to <second_view> for 10 times
    | first_view  | second_view |
    | button_1    | button_2    |
    | button_2    | button_3    |
    | fab         | button_3    |
    | fab         | paint       |

  Scenario: Swipe
    When I swipe in "paint" for 40 times

  Scenario: Pinch and spread
    When I pinch and spread on "paint" for 40 times

  Scenario: Back button
    When "I go back" for 200 times
  
  Scenario: Type with keyboard
    When I type "Physalia says hi!" in "text_field" for 10 times
  
  Scenario: Find By Id
    When I find view with id <view> for 40 times
    | view        |
    | button_1    |
    | button_2    |
    | button_3    |
    | text_field  |
    | fab         |
    | paint       |
    | text_area   |

  Scenario: Find By Description
    When I find view with description <view> for 40 times
    | view          |
    | Button One    |
    | Button Two    |
    | Button Three  |
    | Text Field    |
    | Button Fab    |
    | Paint         |
    | Text Area     |


  Scenario: Find By Content
    When I find view with content <view_content> for 40 times
    | view_content  |
    | Button 1      |
    | Button 2      |
    | Button 3      |
