@controlsurfaces @browser @INTERNAL-ONLY
Feature: Loading ControlSurfaces

  In order to use my MIDI controllers
  As a user
  I want Live to load them properly


  @core
  Scenario Outline: Loading an officially released ControlSurface does not crash Live
    When I open the MIDI preferences
      And the 1st remote script slot has remote script <controller>
    Then the 1st remote script slot holds the '<controller>' control surface

  Examples:
  | controller |
$RELEASED_SCRIPTS$
