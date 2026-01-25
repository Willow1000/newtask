#!/bin/bash
# just a simple setup script to set everything up inside container, you need to change some things here
# change the environment vars at the bottom of the script to your own

export TERM=xterm-color

# shellcheck disable=SC2129
echo "export TERM='$TERM'" >> ~/.bashrc
echo "alias python=python3" >> ~/.bashrc
echo "alias pip=pip3" >> ~/.bashrc

# set vars in /etc/environment
# /usr/bin/env >> /etc/environment  # this doesn't use vars exported in .bashrc
# /usr/bin/env >> /etc/environment sets the root environment variables for all users
echo "TERM=$TERM" >> /etc/environment
export JDK_PATH='/opt/jdk-11.0.6+10'
echo "export JDK_PATH='$JDK_PATH'" >> ~/.bashrc
export JAVA_PATH="$JDK_PATH/bin/"
echo "export JAVA_PATH='$JAVA_PATH'" >> ~/.bashrc
export JAVA_HOME='/opt/jdk-11.0.6+10'
echo "export JAVA_HOME='$JAVA_HOME'" >> ~/.bashrc
# JAVA_HOME='$JDK_PATH' is how it is supposed to be

# TODO (everyone using this container must change this)
# receive from discord bot
echo "export DISCORD_TOKEN=''" >> ~/.bashrc
# send to discord bot
echo "export DISCORD_BOT_TOKEN_OUTGOING=''" >> ~/.bashrc

# dont forget to source the new bash config with the following:
# source $HOME/.bashrc

