# Wiki Path Finder

Wiki game solution implementation. Realised as API.

`GET` request example `http://localhost:45678/path_by_urls?start={start_url}&end={end_url}`
`GET` request example `http://localhost:45678/path_by_names?namespace={namespace}&start={start_name}&end={end_name}`

## Launch in docker

### Building

`docker-compose -p wikipathfinder build`

### Starting

`docker-compose -p wikipathfinder up`

### Exploring

Explore autodocs at http://localhost:45678/docs

### Adding precached data

If API running in the docker, in your project directory will be created `redis-damp` folder, 
it is mounted folder in the docker with redis data dump.

Steps to use your precached data (redis dump file `.rdb`):
1. Stop docker container with app (if running).
2. Create `redis-data` folder in your project directory (if not exists).
3. Place your dump file in data folder with name `dump.rdb`.
4. Start docker compose again.
