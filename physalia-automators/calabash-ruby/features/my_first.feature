Feature: Physalia UI Interactions
  Scenario: swipe
    When I swipe in "paint" for 40 times

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
