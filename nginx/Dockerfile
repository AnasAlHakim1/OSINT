# build stage
FROM node:18-slim as building-stage

WORKDIR /vue-app

# Copy the package.json and install dependencies
COPY ../ OSINT_frontend ./

RUN npm install

# Build the project
RUN npm run build


# production stage
FROM nginx:alpine as production-stage


WORKDIR /

# COPY ./nginx/conf.d/nginx.conf ./etc/nginx/nginx.conf
COPY ./nginx/conf.d/default.conf ./etc/nginx/conf.d/default.conf

## Remove Wfault nginx index page
RUN rm -rf /usr/share/nginx/html/*

# Copy from the stahg 1
COPY --from=building-stage /vue-app/dist /usr/share/nginx/html
# COPY ../dist /usr/share/nginx/html

ENTRYPOINT ["nginx", "-g", "daemon off;"]