# Performance Configuration for USB Physical Security
# Optimized to prevent "Python is not responding" issue

# Real-time status updates - DISABLED to prevent freezing
ENABLE_REAL_TIME_UPDATES = False

# Update intervals (in milliseconds) - Increased for stability
STATUS_UPDATE_INTERVAL = 30000    # 30 seconds instead of 10
GUI_UPDATE_INTERVAL = 2000        # 2 seconds instead of 1

# Registry caching - Enabled to reduce overhead
ENABLE_REGISTRY_CACHING = True
REGISTRY_CACHE_DURATION = 30      # 30 seconds cache

# Admin privilege caching - Enabled to reduce checks
ENABLE_ADMIN_CACHING = True
ADMIN_CACHE_DURATION = 60         # 60 seconds cache

# Error handling
RETRY_ON_ERROR = True
MAX_RETRY_ATTEMPTS = 3
ERROR_RETRY_DELAY = 5000

# GUI responsiveness - Enabled to prevent freezing
ENABLE_GUI_RESPONSIVENESS = True
PROCESS_EVENTS_PERIODICALLY = True

# Performance optimization
USE_EFFICIENT_ADMIN_CHECK = True
MINIMIZE_REGISTRY_ACCESS = True
OPTIMIZE_STATUS_UPDATES = True

# Memory management
ENABLE_MEMORY_OPTIMIZATION = True
CLEANUP_INTERVAL = 60000          # 1 minute cleanup

# Timeout settings
OPERATION_TIMEOUT = 30000
GUI_RESPONSE_TIMEOUT = 10000      # Increased for stability

# Debug mode - Disabled for production
DEBUG_MODE = False
SHOW_PERFORMANCE_INFO = False

# This configuration prevents the "Python is not responding" issue
# by reducing resource usage and improving GUI responsiveness
