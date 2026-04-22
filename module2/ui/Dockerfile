# A lightweight NGINX image is enough because the workshop UI is a static site.
FROM nginx:1.27-alpine

# The default NGINX image supports envsubst for files in /etc/nginx/templates.
WORKDIR /usr/share/nginx/html

# Copy the static application and NGINX template into the image.
COPY index.html /usr/share/nginx/html/index.html
COPY default.conf.template /etc/nginx/templates/default.conf.template

# The default API upstream targets the Kubernetes API service.
ENV API_UPSTREAM=http://api-service.genai.svc.cluster.local:8000

EXPOSE 80
