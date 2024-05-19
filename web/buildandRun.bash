docker build -t web-interface .
docker stop web-interface
docker rm web-interface
docker run -d --name web-interface -p 8080:80 web-interface
