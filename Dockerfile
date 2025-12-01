# Base image with Node.js LTS
FROM node:20-alpine

# Set working directory
WORKDIR /codexdominion

# Copy monorepo files
COPY . .

# Install global tools
RUN npm install -g npm@latest

# Install dependencies for all apps and packages
RUN npm install

# Build all apps and packages
RUN npm run build

# Expose default port for apps (adjust as needed)
EXPOSE 3000

# Default command
CMD ["npm", "start"]