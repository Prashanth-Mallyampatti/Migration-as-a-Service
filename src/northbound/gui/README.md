# Output
Look at the folder output/username/

# Run without Docker
cd into the repo and:
```
npm install
npm start
```

# Run with Docker
## Build Docker Image
```
sudo docker image build .
```

### Find Image ID from:
```
sudo docker images
```
Copy the IMAGE ID

### Run in a container.
```
sudo docker container run --publish <any local host port number>:4000 <copied image id>
```
