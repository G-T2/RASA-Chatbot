# Use the official Rasa Open Source image as the base
FROM rasa/rasa:3.6.20  # Change the version based on your Rasa version

# Set the working directory
WORKDIR /app

# Copy the Rasa project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Train the model
RUN rasa train

# Expose the default Rasa server port
EXPOSE 5005

# Run the Rasa server
CMD ["run", "--enable-api", "--cors", "*", "--debug"]
