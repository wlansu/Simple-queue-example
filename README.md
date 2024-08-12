# Instructions to run the code
For assumptions made see [assumptions.md](docs/assumptions.md).

## Prerequisites
You will need the following installed on your machine:
- Docker
- Make
- Curl
- A browser

## 1. Clone the repository

## 2. Run the following command to build the docker image
```bash
make build
```

## 3. Run the following command to start the docker container
```bash
make up
```

## 4. Run the test suite
```bash
make test
```

## 5. Use the following endpoints to interact with the service
> **_NOTE:_**  You can override the values of hours, minutes, seconds and url in the request body
```bash
# Set a timer
make create_timer HOURS=1 MINUTES=1 SECONDS=1 URL="https://example.com"
```
> **_NOTE:_**  Remember to copy the timer_uuid from the response of the above command and use it in the next command

```bash
# Get a timer
make retrieve_timer TIMER_UUID="55543f48-88fd-4c2b-864f-df306ac5baee"
```
> **_NOTE:_**  This uses a browser to make the request, curl didn't wait for the response. If you're on Linux you will need to replace the `open` command with `xdg-open` or `gnome-open` depending on your desktop environment.


## 6. Run the following command to stop the docker container
```bash
make down
```
