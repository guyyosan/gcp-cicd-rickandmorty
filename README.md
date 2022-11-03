# GCP CI/CD Demo rickandmorty app & Pipeline

## how to build the docker image with Cloud Build
gcloud builds submit -t gcr.io/$GCP_PROJECT/rickandmorty-api .

## Build and deploy with Cloud Build
Trigger is already set on each push to build and deploy.
For best performance use: cloudbuild-optimized.yaml (Cloud build config file)

## Integrate slack
* Create a slack app: https://api.slack.com/apps
* Left menu: Features -> Incoming Webhooks
    * Add New Webhook to Workspace
    * Copy webhooks URL and save it as a secret in Secret Manager
* Update the cloud function secret id in cloud-functions/main.py:7
* Deploy the function

### Deploy cloud function for slack integration
`cd cloud-functions`

`gcloud functions deploy slack_integration --stage-bucket gs://<bucket for cloud functions> --trigger-topic cloud-builds --runtime python38 --ingress-settings internal-only`

## how to run the image with docker
docker run -p 8000:8000 rickandmorty

## rest api endpoints
* /chars/sp/<species>/st/<status>/o/<origin> | methods=["GET"]

example:
`http://0.0.0.0:8000/chars/sp/Human/st/Alive/o/Earth`

* /healthcheck
* /environment
