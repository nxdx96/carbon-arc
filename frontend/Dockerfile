FROM nginx:alpine

# Copy frontend files to nginx html directory
COPY . /usr/share/nginx/html/

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 3000 as specified in requirements
EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]