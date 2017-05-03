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
  end
end
