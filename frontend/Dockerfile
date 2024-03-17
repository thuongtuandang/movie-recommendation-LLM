# Use an official Node runtime as a parent image
FROM node:14

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the package.json and package-lock.json (if available) into the container at /usr/src/app
COPY movie-recommendation/package*.json ./

# Install any needed packages specified in package.json
RUN npm install

# Copy the rest of the frontend's files into the container at /usr/src/app
COPY movie-recommendation/ .

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Define environment variable
ENV REACT_APP_NOT_SECRET_CODE=example_code

# Run npm start when the container launches
CMD ["npm", "start"]
