# Use a base image from jupyter/pyspark-notebook which has Spark and PySpark pre-installed
FROM jupyter/pyspark-notebook:latest

# Install necessary python packages
RUN pip install argparse pyyaml
RUN pip install pyspark

# Set work directory in the docker
WORKDIR /app

# Copy the scripts into the docker image
ADD . /app

# Specify the command to run when the container starts
CMD ["python", "--version"]