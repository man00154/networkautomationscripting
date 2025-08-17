# Use the official Python 3.10 image as a base
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY app.py ./

# Expose the port that Streamlit runs on
EXPOSE 8501

# Command to run the Streamlit app
# The --server.port 8501 and --server.address 0.0.0.0 flags are necessary
# for the app to be accessible outside the container.
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
