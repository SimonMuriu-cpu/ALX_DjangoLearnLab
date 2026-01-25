# Gunicorn configuration for HTTPS deployment

import multiprocessing
import os

# Server socket
bind = "unix:/path/to/your/project/gunicorn.sock"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# Server mechanics
daemon = False
pidfile = '/path/to/your/project/gunicorn.pid'
umask = 0o022
user = None
group = None
tmp_upload_dir = None

# Logging
accesslog = '/path/to/your/project/logs/gunicorn_access.log'
errorlog = '/path/to/your/project/logs/gunicorn_error.log'
loglevel = 'info'

# Process naming
proc_name = 'library_project'

# SSL Configuration (if running Gunicorn with SSL directly)
# keyfile = '/path/to/ssl/key.pem'
# certfile = '/path/to/ssl/cert.pem'

# Server hooks
def pre_fork(server, worker):
    pass

def post_fork(server, worker):
    pass

def pre_exec(server):
    server.log.info("Server is forked")

def when_ready(server):
    server.log.info("Server is ready. Spawning workers")

def worker_int(worker):
    worker.log.info("Worker received INT or QUIT signal")

def worker_abort(worker):
    worker.log.info("Worker received SIGABRT signal")