FROM nginx:1.15-alpine

RUN rm /etc/nginx/conf.d/default.conf

# create sites-enabled -- not in alpine/nginx
ADD sites-enabled/ /etc/nginx/sites-enabled

# copy local version of nginx config
COPY nginx.conf  /etc/nginx/

# create SSL dir for certs
RUN mkdir /etc/nginx/ssl

# add packages not available in Alpine
RUN apk update && apk add nano
RUN apk update && apk add bash
