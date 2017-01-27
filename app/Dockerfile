FROM python:2.7

ENV PYTHONUNBUFFERED 1

# Make app directory for code etc
RUN mkdir /app

# Set working directory to app
WORKDIR /app

# Copy Python package requirements
ADD requirements.txt requirements.txt

# Install Python Packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django app
ADD django django

# Copy Gunicorn Config app
ADD gunicorn_conf.py gunicorn_conf.py

# Copy check_db.py script
ADD check_db.py check_db.py

# Copy entrypoint script into the image
ADD docker-entrypoint.sh /

# Set entrypoint script
ENTRYPOINT ["/docker-entrypoint.sh"]
