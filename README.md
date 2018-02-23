# rabbitmq-job-spawner

## Description:

A proof of concept RabbitMQ based kubernetes job spawner.

## Installation

1. `export DOCKER_USERNAME=myDockerHubUsername`
2. `python3 -m venv .`
3. `source bin/activate`
4. (optional, for locally testing) `pip install -r requirements.txt`
5. `./build-docker-images.sh` (will also try to push to docker hub…)
6. `kubectl apply -f src/listener.yaml` (important: make sure the blob storage secrets are in place!)
7. submit some rabbitmq jobs. use `producer.py` to submit them.
8. watch as your cluster spins up Job workloads as defined by `workloads/encoder.json`!


## License

MIT. See License file.