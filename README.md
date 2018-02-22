# rabbitmq-job-spawner

## Description:

A proof of concept RabbitMQ based kubernetes job spawner.

## Installation

1. `export DOCKER_USERNAME=myDockerHubUsername`
2. `python3 -m venv .`
3. `source bin/activate`
4. (optional, for locally testing) `pip install -r requirements.txt`
5. `./build-docker-images.sh` (will also try to push to docker hub…)
6. `kubectl apply -f src/listener.yaml`
7. submit some rabbitmq jobs to a queue in this JSON format as a string:

```
    {
        'encoding_type': '',
        'file_name': '',
        'file_loc': ''
    }
```
8. watch as your cluster spins up Job workloads as defined by `src/noop.yaml`!


## License

MIT. See License file.