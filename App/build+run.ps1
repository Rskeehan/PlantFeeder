cd "C:\Users\RPS00\OneDrive\Documents\03 Coding\PlantFeeder\App"
docker build -t plant-feeder .
docker run -d --env-file .env plant-feeder