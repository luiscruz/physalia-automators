Feature: Physalia UI Interactions

  Scenario: Tap on views
    When I tap <view> for 40 times
    | view    |
    | button_1  |
    | button_2  |
    | button_3  |
    | fab       |

  Scenario: Long tap on views
    When I long tap <view> for 40 times
    | view    |
    | button_1  |
    | button_2  |
    | button_3  |
    | fab       |

  Scenario: Dragndrop
    When I dragndrop <first_view> to <second_view> for 40 times
    | first_view  | second_view |
    | button_1    | button_2    |
    | fab         | button_3    |
    | fab         | button_3    |
    | fab         | text_area   |

  Scenario: Swipe
    When I swipe in "paint" for 40 times

  Scenario: Pinch and spread
    When I pinch and spread on "paint" for 40 times

  Scenario: Back button
    When "I go back" for 40 times
