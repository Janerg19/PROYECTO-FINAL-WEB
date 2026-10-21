# Multi-stage build para frontend con nginx

# Stage 1: Copy assets
FROM alpine:latest AS builder

WORKDIR /app

# Copiar assets desde el contexto
COPY public /usr/share/nginx/html

# Stage 2: Run with nginx
FROM nginx:alpine

# Copiar configuración nginx
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# Copiar assets desde builder
COPY --from=builder /usr/share/nginx/html /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
