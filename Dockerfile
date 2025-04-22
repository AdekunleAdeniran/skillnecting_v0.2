# Use a specific Python version
FROM python:3.8

# Set a working directory inside the container
WORKDIR /app

# Install system dependencies and upgrade pip
RUN apt update && apt upgrade -y
RUN pip install --upgrade pip

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy all other project files into the working directory
COPY . .

# Define entry point
ENTRYPOINT ["python"]
CMD ["run.py"]

# Expose port for the app
EXPOSE 5000
