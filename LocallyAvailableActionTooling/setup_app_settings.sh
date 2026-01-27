#!/bin/bash
# just a simple setup script to set everything up inside container, you need to change some things here
# change the environment vars at the bottom of the script to your own

# HOW TO USE:
#  the problem with this script is that it replaces settings on most apps, meaning you have to execute 
#   those apps first(such that these apps create their own default settings), 
#    which is annoying to do, makes it hard to use this script

export TERM=xterm-color
 
# setup settings for all apps

# setup runelite settings
rm -rf ~/.runelite/profiles2
mkdir ~/.runelite/profiles2
cp /opt/code/LocallyAvailableActionTooling/all_app_profiles/rs_profiles/default* ~/.runelite/profiles2/
cp /opt/code/LocallyAvailableActionTooling/all_app_profiles/rs_profiles/profiles.json ~/.runelite/profiles2/


