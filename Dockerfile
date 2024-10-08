# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create the Streamlit configuration folder
RUN mkdir -p ~/.streamlit

# Copy your config.toml into the Streamlit config directory
COPY config.toml ~/.streamlit/config.toml

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the app will run on
EXPOSE 8501

# Run the application when the container launches
CMD ["streamlit", "run", "gai-helpers/app.py", "--server.baseUrlPath=/gai-helpers"]