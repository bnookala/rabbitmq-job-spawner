docker build . -t rabbitmq-listener -f ./src/Dockerfile.listener
docker tag rabbitmq-listener $DOCKER_USERNAME/rabbitmq-listener
docker push $DOCKER_USERNAME/rabbitmq-listener