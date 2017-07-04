require 'calabash-android/calabash_steps'
require 'pry'

When(/^I tap <view> for (\d+) times$/) do |times, table|
  times.to_i.times do
    table.hashes.each do |row|
      id = row['view']
      tap_when_element_exists("* id:'#{id}'")
    end
  end
end

When(/^I long tap <view> for (\d+) times$/) do |times, table|
  times.to_i.times do
    table.hashes.each do |row|
      id = row['view']
      long_press_when_element_exists("* id:'#{id}'")
    end
  end
end

When(/^I dragndrop <first_view> to <second_view> for (\d+) times$/) do |times, table|
  times.to_i.times do
    table.hashes.each do |row|
      first_view = row['first_view']
      second_view = row['second_view']
      drag_and_drop(
        "* id:'#{first_view}'", "* id:'#{second_view}'",
        steps=10, hold_time=0.5, hang_time=0.5)
    end
  end
end

When(/^I swipe in "([^"]*)" for (\d+) times$/) do |view, times|
  times.to_i.times do
    pan "* id:'#{view}'", :left
    pan "* id:'#{view}'", :right
  end
end

When(/^I pinch and spread on "([^"]*)" for (\d+) times$/) do |view, times|
  times.to_i.times do 
    pinch "* id:'#{view}'", :in
    pinch "* id:'#{view}'", :out
  end
end

When(/^"([^"]*)" for (\d+) times$/) do |nested_step, times|
  times.to_i.times do
    step nested_step
    sleep 0.1
  end
end

When(/^I type "([^"]*)" in "([^"]*)" for (\d+) times$/) do |text_to_enter, text_field, times|
  times.to_i.times do
    enter_text("* id:'#{text_field}'", text_to_enter)
    clear_text_in("* id:'#{text_field}'")
  end
end

When(/^I find view with id <view> for (\d+) times$/) do |times, table|
  times.to_i.times do
    table.hashes.each do |row|
      execute_uiquery("* id:'#{row['view']}'")
    end
  end
end

When(/^I find view with description <view> for (\d+) times$/) do |times, table|
  times.to_i.times do
    table.hashes.each do |row|
      execute_uiquery("* contentDescription:'#{row['view']}'")
    end
  end
end

When(/^I find view with content <view_content> for (\d+) times$/) do |times, table|
  times.to_i.times do
    table.hashes.each do |row|
      execute_uiquery("* text:'#{row['view_content']}'")
    end
  end
end
