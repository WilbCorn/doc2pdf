FROM alpine:3.18
# FROM ubuntu:22.04

# Install Python and LibreOffice

## This is for ubuntu
# RUN apt-get update && \
#     apt-get install -y python3 python3-pip libreoffice && \
#     apt-get clean

RUN apk add --no-cache libreoffice python3 py3-pip openjdk8-jre

# Set work directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip3 install -r gui_requirements.txt

# Set entrypoint
ENTRYPOINT ["streamlit", "run", "gui_main.py", "--server.port=8501", "--server.address=0.0.0.0"]