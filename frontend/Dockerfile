# NODE image used to build the application
FROM node:11-alpine as builder
WORKDIR /home

RUN apk add yarn
RUN apk add --no-cache git

COPY public/ app/public
COPY src/ app/src
COPY package.json yarn.lock app/
COPY .env.production app/

WORKDIR /home/app
RUN yarn && yarn build

# NGINX image
FROM nginx:1.15-alpine
COPY --from=builder /home/app/build /var/www
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]