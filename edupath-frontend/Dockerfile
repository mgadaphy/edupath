# Build stage
FROM node:18-alpine AS build

# Set working directory
WORKDIR /app

# Copy package files first to leverage Docker cache
COPY edupath-frontend/package*.json edupath-frontend/pnpm-lock.yaml* ./

# Install pnpm
RUN npm install -g pnpm

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy the rest of the application
COPY edupath-frontend/ .

# Build the app
RUN pnpm run build

# Production stage
FROM nginx:alpine

# Copy built assets from build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx config
COPY edupath-frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
