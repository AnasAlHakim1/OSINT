bind = '0.0.0.0:8000'  # The address and port for Gunicorn to bind to
timeout = 43200  # Request timeout in seconds (12 hours)
max_requests = 1000  # Number of requests a worker will process before restarting

# Logging
accesslog = '/var/log/access.log'
errorlog = '/var/log/error.log'
loglevel = 'info'