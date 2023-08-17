# Use an official Python runtime
FROM python:3.10

# Set environment variables
ENV PYTHONWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app 

# Copy the requirements file into app container dir
COPY requirements.txt /app/

# Install dependencies from requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy the content of the local dir into app dir
COPY . /app/

# Expose port 8000 for the Django app server
EXPOSE 8000

# Define the command to run the application
CMD [ "gunicorn", "bookstore.wsgi:application", "--bind", "0.0.0.0:8000" ]
