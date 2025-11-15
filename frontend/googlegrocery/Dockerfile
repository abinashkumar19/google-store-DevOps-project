FROM nginx:alpine

# remove any default files
RUN rm -rf /usr/share/nginx/html/*

# copy only static assets
COPY index.html style.css script.js /usr/share/nginx/html/

# copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
