# Extend the official Rasa SDK image
FROM rasa/rasa-sdk:2.5.0

# Use subdirectory as working directory
WORKDIR /app

# Copy any additional custom requirements, if necessary (uncomment next line)
COPY requirements-actions.txt ./

# Change back to root user to install dependencies
USER root

# Install extra requirements for actions code, if necessary (uncomment next line)
RUN pip install -r requirements-actions.txt

# Copy actions folder to working directory
COPY . /app/actions

# RUN chmod +x /app/actions/action_server.sh
# CMD /app/actions/action_server.sh

# Back to user mode
USER 1001
