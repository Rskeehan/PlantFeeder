cd "C:\Users\RPS00\OneDrive\Documents\03 Coding\PlantFeeder\App"
docker build -t app .
docker run -d --name app --env-file .env app