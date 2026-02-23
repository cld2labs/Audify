FROM node:18

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY --chown=node:node package.json ./
COPY --chown=node:node package-lock.json ./

RUN chown -R node:node /app
USER node

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY --chown=node:node . .

# Expose the port the app runs on
EXPOSE 3000

# Command to run the application
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
