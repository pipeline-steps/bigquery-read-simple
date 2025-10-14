# bigquery-read-simple

Reading a bigquery table (simple version)

## Docker Image

This application is available as a Docker image on Docker Hub: `pipelining/bigquery-read-simple`

### Usage

```bash
docker run -v /path/to/config.json:/config.json \
           -v /path/to/output:/output \
           -v /path/to/credentials.json:/credentials.json \
           -e GOOGLE_APPLICATION_CREDENTIALS=/credentials.json \
           pipelining/bigquery-read-simple:latest \
           --config /config.json \
           --output /output/data.jsonl
```

To see this documentation, run without arguments:
```bash
docker run pipelining/bigquery-read-simple:latest
```

## Parameters

| Name           | Required | Description                                                        |
|----------------|----------|--------------------------------------------------------------------|
| billingProject | X        | the GCP project id to be used as quota project                     |
| inputTable     |          | bigquery table (or view) to be read (format project.dataset.table) |
| query          |          | select query to be executed ("SELECT ...")                         |

**Notes:**
  * billingProject: the user/service account needs to have bigquery.jobs.create permission on this project
  * inputTable: the user/service account needs to have bigquery.tables.getData permission on this table/view
  * query: the user/service account needs to have bigquery.tables.getData permission on the queried table(s)/view(s)
  * you must specify either a `ìnputTable` or `query` (not both)
