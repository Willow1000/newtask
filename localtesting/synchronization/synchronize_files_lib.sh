#!/bin/bash

set -euo pipefail
CONFIG_FILE=""
LOG_FILE="/tmp/multi_rsync_monitor.log"
# RSYNC_OPTIONS="-avz --delete"  # no default options is better, forces to add this arguments
REMOTE_HOST=""  # user@host format
declare -A SYNC_PAIRS
declare -A MONITOR_PIDS
EXCLUDE_PATTERNS=("venv/")
 
# TEMP_FILE_EXECUTION_INFO_FILE this directory will hold temporary files that hold execution info for each sync pair 
 # the execution info consists of ip, unique id of the sync pair (based on the hash of the sync pairs file)
  # purpose of this execution info is to avoid multiple instances of the same sync pair monitor running at the same time
   # it's useful to avoid I dont want more rsync connections than needed
TEMP_FILE_EXECUTION_INFO_FILE="$HOME/synchronize_files_with_rsync_execution_info_files_dir/"
mkdir -p "$TEMP_FILE_EXECUTION_INFO_FILE"
 
log_message() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

construct_remote_path() {
    local remote_path="$1"
    if [[ -n "$REMOTE_HOST" ]]; then
      echo "${REMOTE_HOST}:${remote_path}"
    else
      echo "$remote_path"
    fi
}

parse_config_file() {
    local config_file="$1"
    if [[ ! -f "$config_file" ]]; then
      log_message "ERROR: Configuration file '$config_file' not found"
      exit 1
    fi
    log_message "Parsing configuration file: $config_file"
    local line_num=0
    while IFS= read -r line || [[ -n "$line" ]]; do
      line_num=$((line_num + 1))
      echo $line
      # Skip empty lines and comments
      if [[ -z "$line" ]] || [[ "$line" =~ ^[[:space:]]*# ]]; then
        continue
      fi
      # Handle configuration options (but RSYNC_OPTIONS from file will be overridden by command line)
      if [[ "$line" =~ ^[[:space:]]*([A-Z_]+)[[:space:]]*=[[:space:]]*(.+)$ ]]; then
        local key="${BASH_REMATCH[1]}"
        local value="${BASH_REMATCH[2]}"
        case "$key" in
          "RSYNC_OPTIONS")
            # Only use from config file if not provided via command line
            if [[ "$RSYNC_OPTIONS" == "-avz --delete" ]]; then
              RSYNC_OPTIONS="$value"
              echo "rsync options: $RSYNC_OPTIONS"
              log_message "Set RSYNC_OPTIONS from config: $value"
            else
              log_message "RSYNC_OPTIONS from command line overrides config file"
            fi
            ;;
          "LOG_FILE")
            LOG_FILE="$value"
            ;;
          "EXCLUDE")
            EXCLUDE_PATTERNS+=("$value")
            log_message "Added exclude pattern: $value"
            ;;
          "REMOTE_HOST")
            # Only use from config file if not provided via command line
            if [[ -z "$REMOTE_HOST" ]]; then
              REMOTE_HOST="$value"
              log_message "Set REMOTE_HOST from config: $value"
            else
              log_message "REMOTE_HOST from command line overrides config file"
            fi
            ;;
        esac
        continue
      fi
      # Handle sync pairs (local_path:remote_path format)
      if [[ "$line" =~ ^[[:space:]]*(.+)[[:space:]]*:[[:space:]]*(.+)[[:space:]]*$ ]]; then
        local local_path="${BASH_REMATCH[1]}"
        local remote_path="${BASH_REMATCH[2]}"
          # Expand tilde and environment variables for local path
          local_path=$(eval echo "$local_path")
          # Check if local path exists (source directory)
          if [[ ! -d "$local_path" ]]; then
            log_message "WARNING: Local directory '$local_path' does not exist (line $line_num)"
            continue
          fi
          # Construct full destination path
          local full_dest
          if [[ -n "$REMOTE_HOST" ]]; then
            full_dest=$(construct_remote_path "$remote_path")
            log_message "Remote sync pair detected"
          else
            # Local sync - expand variables and create directory if needed
            full_dest=$(eval echo "$remote_path")
            if [[ ! -d "$full_dest" ]]; then
              log_message "Creating local destination directory: $full_dest"
              mkdir -p "$full_dest" || {
                log_message "ERROR: Failed to create destination directory '$full_dest'"
                                continue
                              }
            fi
          fi
          SYNC_PAIRS["$local_path"]="$full_dest"
          log_message "Added sync pair: '$local_path' -> '$full_dest'"
      fi
    done < "$config_file"
    if [[ ${#SYNC_PAIRS[@]} -eq 0 ]]; then
      log_message "ERROR: No valid sync pairs found in configuration file"
      exit 1
    fi
    log_message "Loaded ${#SYNC_PAIRS[@]} sync pairs"
    if [[ -n "$REMOTE_HOST" ]]; then
      log_message "Remote host: $REMOTE_HOST"
    else
      log_message "Mode: Local sync only"
    fi
}
 
sync_directory_pair() {
    local source="$1"
    local dest="$2"
    local trigger_file="${3:-manual}"
    log_message "Syncing: '$source' -> '$dest' (triggered by: $trigger_file)"
    # Build exclude options
    local exclude_opts=""
    for pattern in "${EXCLUDE_PATTERNS[@]}"; do
      exclude_opts+="--exclude=$pattern "
    done
    # Build full rsync command
    local rsync_cmd="rsync $RSYNC_OPTIONS $exclude_opts"
    # Add trailing slash to source directory
    local sync_source="$source/"
    local sync_dest="$dest/"
    # Log the actual command being executed (with sensitive info masked)
    # local masked_cmd=$(echo "$rsync_cmd" | sed 's/-i [^ ]*/-i [SSH_KEY]/g')
    # log_message "Executing: $masked_cmd '$sync_source' '$sync_dest'"
    log_message "Executing: \"$rsync_cmd\" \"$sync_source\" \"$sync_dest\""
    # Perform sync with error handling
    if eval "$rsync_cmd \"$sync_source\" \"$sync_dest\"" 2>>"$LOG_FILE"; then
      log_message "✓ Sync completed: '$source' -> '$dest'"
      return 0
    else
      local exit_code=$?
      log_message "✗ Sync failed: '$source' -> '$dest' (exit code: $exit_code)"
        # Log specific rsync error meanings
        case $exit_code in
          1) log_message "Error: Syntax or usage error" ;;
          2) log_message "Error: Protocol incompatibility" ;;
          3) log_message "Error: Errors selecting input/output files, dirs" ;;
          4) log_message "Error: Requested action not supported" ;;
          5) log_message "Error: Error starting client-server protocol" ;;
          10) log_message "Error: Error in socket I/O" ;;
          11) log_message "Error: Error in file I/O" ;;
          12) log_message "Error: Error in rsync protocol data stream" ;;
          13) log_message "Error: Errors with program diagnostics" ;;
          14) log_message "Error: Error in IPC code" ;;
          20) log_message "Error: Received SIGUSR1 or SIGINT" ;;
          21) log_message "Error: Some error returned by waitpid()" ;;
          22) log_message "Error: Error allocating core memory buffers" ;;
          23) log_message "Error: Partial transfer due to error" ;;
          24) log_message "Error: Partial transfer due to vanished source files" ;;
          25) log_message "Error: The --max-delete limit stopped deletions" ;;
          30) log_message "Error: Timeout in data send/receive" ;;
          35) log_message "Error: Timeout waiting for daemon connection" ;;
          *) log_message "Error: Unknown rsync error code: $exit_code" ;;
        esac
        return 1
    fi
}

setup_ssh_agent() {
    local ssh_key_path="$1"
    eval "$(ssh-agent -s)"
     
    # Check if key is already loaded
    if ! ssh-add -l | grep -q "$ssh_key_path"; then
        echo "Adding SSH key to agent..."
        ssh-add "$ssh_key_path"
        if [ $? -eq 0 ]; then
            echo "SSH key successfully added to agent"
        else
            echo "Failed to add SSH key to agent"
            exit 1
        fi
    else
        echo "SSH key already loaded in agent"
    fi
}

monitor_directory() {
    local source="$1"
    local dest="$2"
    local output_file="/tmp/rsync_monitor_$(date +%Y%m%d_%H%M%S)_$(echo "$source" | md5sum | awk '{print $1}').log"
    log_message "Starting monitor for: $source"
     
    inotifywait -m -r -e modify,create,delete,move,moved_to,moved_from "$source" \
      --format '%w%f %e' 2>/dev/null | tee -a "$output_file" |
      while read -r file event; do
        # Skip temporary and hidden files
        if [[ "$file" =~ \.(tmp|swp|~|bak)$ ]] || \
          [[ "$(basename "$file")" =~ ^\. ]] || \
          [[ "$file" =~ /__pycache__/ ]] || \
          [[ "$file" =~ /\.git/ ]] || \
          [[ "$file" =~ /node_modules/ ]]; then
                  continue
        fi
        # Additional filtering for common temporary files
        local filename=$(basename "$file")
        if [[ "$filename" =~ ^\.#.*$ ]] || \
          [[ "$filename" =~ ^#.*#$ ]] || \
          [[ "$filename" =~ .*\.tmp$ ]] || \
          [[ "$filename" =~ .*\.lock$ ]]; then
                  continue
        fi
        sleep 0.3
        # Sync the directory pair
        sync_directory_pair "$source" "$dest" "$file"
        # flush
        sync
      done &
    # Store the PID for this monitor
    MONITOR_PIDS["$source"]=$!
    log_message "Monitor started for '$source' with PID: ${MONITOR_PIDS["$source"]}"
}

start_all_monitors() {
    log_message "Starting monitors for all configured directories..."
    log_message "Using RSYNC_OPTIONS: $RSYNC_OPTIONS"
     
    local started_monitors=0
    for source in "${!SYNC_PAIRS[@]}"; do
      dest="${SYNC_PAIRS[$source]}"
      if monitor_directory "$source" "$dest"; then
        started_monitors=$((started_monitors + 1))
      fi
    done
    log_message "Started $started_monitors monitors for ${#SYNC_PAIRS[@]} configured pairs."
    log_message "Press Ctrl+C to stop monitoring."
    show_status
}

stop_all_monitors() {
    log_message "Stopping all monitors..."
    for source in "${!MONITOR_PIDS[@]}"; do
      local pid="${MONITOR_PIDS[$source]}"
      if kill -0 "$pid" 2>/dev/null; then
        kill "$pid" 2>/dev/null
        log_message "Stopped monitor for: $source (PID: $pid)"
      fi
    done
    pkill -f "inotifywait" 2>/dev/null || true
    log_message "All monitors stopped."
}

show_status() {
    echo ""
    echo "=== Multi-Directory Rsync Monitor Status ==="
    echo "Configuration file: $CONFIG_FILE"
    echo "Remote host: ${REMOTE_HOST:-'None (local sync only)'}"
    echo "Log file: $LOG_FILE"
    echo "Rsync options: $RSYNC_OPTIONS"
    echo ""
    echo "Monitored directories:"
    printf "%-50s -> %-50s [%s]\n" "LOCAL PATH" "DESTINATION" "STATUS"
    printf "%-50s -> %-50s [%s]\n" "$(printf '%*s' 50 '' | tr ' ' '-')" "$(printf '%*s' 50 '' | tr ' ' '-')" "$(printf '%*s' 20 '' | tr ' ' '-')"
    for source in "${!SYNC_PAIRS[@]}"; do
      dest="${SYNC_PAIRS[$source]}"
      local pid="${MONITOR_PIDS[$source]:-N/A}"
      local status="STOPPED"
      if [[ "$pid" != "N/A" ]] && kill -0 "$pid" 2>/dev/null; then
        status="RUNNING (PID: $pid)"
      fi
      printf "%-50s -> %-50s [%s]\n" "$source" "$dest" "$status"
    done
    echo ""
    echo "Exclude patterns: ${EXCLUDE_PATTERNS[*]:-none}"
    echo "Current time: $(date -u '+%H:%M')"
    echo "=== End Status ==="
    echo ""
}

show_usage() {
    cat << EOF
Multi-Directory Rsync Monitor with SSH Support
USAGE:
    $0 [OPTIONS] <config_file>
OPTIONS:
    --remote-host USER@HOST Remote host for SSH sync (user@hostname format)
    --rsync-options OPTS    Rsync options (required for SSH key specification)
    --log-file FILE         Log file path
    --create-sample         Create a sample configuration file
    --help                 Show this help message
DESCRIPTION:
    Monitors multiple local directories for changes and syncs them in real-time
    using rsync. Supports SSH with key authentication for remote sync.
    The config file contains local_path:remote_path pairs. The remote host
    (user@hostname) is specified once via --remote-host argument.
CONFIGURATION FILE FORMAT:
    # Comments start with #
    local_path : remote_path
    # Optional global settings:
    RSYNC_OPTIONS = -avz --delete --progress
    REMOTE_HOST = user@hostname
    LOG_FILE = /path/to/logfile
    EXCLUDE = pattern_to_exclude
EXAMPLES:
    # Remote sync with SSH key
    $0 --remote-host backup@server.com \\
       --rsync-options '-avz --delete -e "ssh -i ~/.ssh/backup_key"' \\
       sync_config.conf
    # Remote sync with custom SSH port and options
    $0 --remote-host user@backup.example.com \\
       --rsync-options '-avz --delete -e "ssh -i ~/.ssh/backup_key -p 2222 -o StrictHostKeyChecking=no"' \\
       sync_config.conf
    # Local sync only (no remote host)
    $0 --rsync-options '-avz --delete --progress' \\
       local_sync_config.conf
    # With bandwidth limiting and custom log
    $0 --remote-host backup@server.com \\
       --rsync-options '-avz --delete --bwlimit=5000 -e "ssh -i ~/.ssh/backup_key"' \\
       --log-file /var/log/my_backup.log \\
       sync_config.conf
    # Create sample configuration
    $0 --create-sample
SSH SETUP:
    1. Generate SSH key: ssh-keygen -t rsa -b 4096 -f ~/.ssh/backup_key
    2. Copy to remote: ssh-copy-id -i ~/.ssh/backup_key.pub user@host
    3. Set permissions: chmod 600 ~/.ssh/backup_key
    4. Test connection: ssh -i ~/.ssh/backup_key user@host
CONFIG FILE EXAMPLE:
    # Exclude patterns
    EXCLUDE=*.tmp
    EXCLUDE=.git/
    # Sync pairs
    /home/user/docs : /backup/documents
    /var/www : /backup/websites
    ~/projects : /backup/code
SIGNALS:
    SIGINT/SIGTERM   Gracefully stop all monitors
    SIGUSR1          Show status of all monitors
NOTES:
    - SSH keys should have 600 or 400 permissions
    - Command-line options override config file options
    - Local paths must exist before starting
    - Remote directories will be created automatically by rsync
    - Use absolute paths in config file for reliability
EOF
}
 
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --remote-host)
                if [[ -z "${2:-}" ]]; then
                    echo "ERROR: --remote-host requires a value (user@hostname format)"
                    exit 1
                fi
                if [[ ! "$2" =~ ^[^@]+@[^@]+$ ]]; then
                    echo "ERROR: --remote-host must be in user@hostname format"
                    exit 1
                fi
                REMOTE_HOST="$2"
                log_message "REMOTE_HOST set via command line: $REMOTE_HOST"
                shift 2
                ;;
            --rsync-options)
                if [[ -z "${2:-}" ]]; then
                    echo "ERROR: --rsync-options requires a value"
                    exit 1
                fi
                RSYNC_OPTIONS="$2"
                log_message "RSYNC_OPTIONS set via command line: $RSYNC_OPTIONS"
                shift 2
                ;;
            --log-file)
                if [[ -z "${2:-}" ]]; then
                    echo "ERROR: --log-file requires a value"
                    exit 1
                fi
                LOG_FILE="$2"
                shift 2
                ;;
            --create-sample)
                create_sample_config
                exit 0
                ;;
            --help|-h)
                show_usage
                exit 0
                ;;
            -*)
                echo "ERROR: Unknown option: $1"
                show_usage
                exit 1
                ;;
            *)
                if [[ -z "$CONFIG_FILE" ]]; then
                    CONFIG_FILE="$1"
                else
                    echo "ERROR: Multiple config files specified"
                    exit 1
                fi
                shift
                ;;
        esac
    done
}

validate_arguments() {
    if [[ -z "$CONFIG_FILE" ]]; then
        echo "ERROR: Configuration file required"
        show_usage
        exit 1
    fi
    if [[ ! -f "$CONFIG_FILE" ]]; then
        echo "ERROR: Configuration file '$CONFIG_FILE' not found"
        exit 1
    fi
    if [[ -n "$REMOTE_HOST" ]] && [[ ! "$RSYNC_OPTIONS" =~ -e.*ssh ]]; then
        echo "WARNING: Remote host specified but no SSH options found in rsync options"
        echo "You may want to add: -e \"ssh -i /path/to/key\""
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

create_hash_from_file() {
  # returns hash from contents of file
  local file_path="$1"
  if [[ -f "$file_path" ]]; then
    sha256sum "$file_path" | cut -d' ' -f1
  else
    echo ""
  fi
}



