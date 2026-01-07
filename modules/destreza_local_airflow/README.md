# Local Airflow Setup - 'Destreza'

Basic instructions for how to run an Airflow instance on local Docker.
It's easier than you think.

'Destreza' is a placeholder name to avoid confusion with other projects.

## Running Airflow on Docker

I pulled the image with:

```docker pull apache/airflow:3.1.5```

and spun up a container with:

```docker run -d -p 8080:8080 --name destreza-container apache/airflow:3.1.5 standalone```.

Port 8080 is exposed for the Airflow dashboard (served at `localhost:8080`).
If your container booted successfully,
you should see authentication details in the logs.

```
standalone | Starting Airflow Standalone
Simple auth manager | Password for user 'admin': pzM7PWshnN5QTu4h
standalone | Checking database is initialized
standalone | Database ready
...
```

While access to the dashboard isn't mandatory,
it is very convenient and provides a lot of functionality
(logs, job history, etc)
that just doesn't exist in the CLI.

### Accessing the Container Shell

You can shell into the container with:

```docker exec -it destreza-container sh```

or by using the docker desktop UI.
This should put you in the `$AIRFLOW_HOME` directory (`/opt/airflow` by default).

In this directory is an `airflow.cfg` which contains all the Airflow settings.
Most notable is the `dags_folder = [...]` line.
This is the folder Airflow watches to find your DAGs (`/opt/airflow/dags` by default).

### DAG Execution

After creating a python file with your DAG definition,
place it inside the DAGs folder on the airflow instance.
From the host machine:

```
docker cp dag.py destreza-container:/opt/airflow/dags
```

In theory, it should now be ready to run in the webserver dashboard.
In practice, whatever subprocess is responsible for watching the DAG folder is kinda slow.
You can either wait for the DAG to appear on the dashboard (takes up to a few minutes),
or force an update with `airflow dags list` (forces Airflow to parse the folder contents).

Alternatively, just run the DAG manually:

```
airflow dags trigger destreza_dag
```

Again, the CLI is quite limited and I would avoid it whenever possible.
But it's there if you need it.