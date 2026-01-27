!#/bin/bash 

# must install ruff first with: pip3 install ruff
ruff format ../runescape_actions/runescape_actions/* --config ruff/ruff.toml
ruff format ../runescape_actions/reusable_actions/reusable_actions/* --config ruff/ruff.toml 
ruff format ../runescape_actions/common_action_framework/common_action_framework/* --config ruff/ruff.toml


