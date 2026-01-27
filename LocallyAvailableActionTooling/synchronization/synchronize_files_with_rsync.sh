#!/bin/bash

# Multi-Directory Rsync Monitor Script with SSH support
# Usage: ./multi_rsync_monitor.sh [OPTIONS] <config_file>

# Source the synchronize_files_lib.sh library
filename="$(dirname "${BASH_SOURCE[0]}")/synchronize_files_lib.sh" 
source "$filename"
 
main() {
    if [[ $# -eq 0 ]]; then
        echo "ERROR: Arguments required"
        show_usage
        exit 1
    fi
    # Parse command line arguments
    parse_arguments "$@"
    local ssh_key_path=$(echo "$RSYNC_OPTIONS" | sed -n 's/.*ssh -i \([^ ]*\).*/\1/p')
    setup_ssh_agent "${ssh_key_path}"

    # in case any rsync processes are leftover: use this command: 
     # sudo ps -auxww | grep rsync | grep -v grep | awk '{print $2}' | xargs sudo kill -9
    sync_pair_hash=$(create_hash_from_file "$CONFIG_FILE")
    sync_pair_hash_first_15_chars="${sync_pair_hash:0:25}"  # first 25 chars from hash for filename
    filename="${TEMP_FILE_EXECUTION_INFO_FILE}/${sync_pair_hash_first_15_chars}"
    >&2 echo "DEBUGPRINT[410]: synchronize_files_with_rsync.sh:487: filename=${filename}"
    if [ -f "$filename" ]; then
        file_content=$(cat "$filename")
        if ps -p "$file_content" > /dev/null 2>&1; then
            echo "sync associated with this sync pair is already running, quitting..."
            exit
        else
            echo "no longer running the sync associated with this sync pair, proceding to start new sync pair"
        fi
    else
        echo "sync associated with this sync pair is not running yet"
    fi
    process_id=$$
    echo "$process_id" > "$filename"

    validate_arguments

    log_message "=== Multi-Directory Rsync Monitor Starting ==="
    log_message "PID: $$"
    log_message "Config file: $CONFIG_FILE"
    log_message "Remote host: ${REMOTE_HOST:-'None (local sync only)'}"
    log_message "Log file: $LOG_FILE"

    parse_config_file "$CONFIG_FILE"
    start_all_monitors

    # Wait for monitors (keep script running)
    while true; do
        sleep 3600
    done
}

# Signal handlers
trap 'stop_all_monitors; exit 0' SIGINT SIGTERM
trap 'show_status' SIGUSR1

main "$@"


