#!/bin/bash
export TERM=xterm-color

if [[ -z "${SETUP_ONCE}" ]]; then
  # the following executes if $SETUP_ONCE is not set
  export SETUP_ONCE="setup once check"
  echo "export SETUP_ONCE='$SETUP_ONCE'" >> ~/.bashrc
else
  # at the start always deletes previous X11 locks, in case a crash happened, this can be really annoying
  #  therefore, it must be deleted
  echo 'already setup once, skipping setup'
  rm -rf /tmp/.X1-lock
  rm -rf /tmp/.X11-unix
  # auto start download logs service 
  #  (remember to set the environment variable in setup_container script for this to work)
  /code/venv_inside_docker/bin/python3 /opt/code/LocallyAvailableActionTooling/unzip_from_discord_script.py --out_data="/workspace" run > /dev/null 2>&1 &
  echo 'started auto log service'
fi

/bin/bash -i


