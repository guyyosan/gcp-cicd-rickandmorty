# GCP CI/CD Demo rickandmorty app & Pipeline

### how to build the docker image
gcloud builds submit -t gcr.io/$GCP_PROJECT/rickandmorty-api .

docker build . -t rickandmorty

### how to run the image
docker run -p 8000:8000 rickandmorty

### rest api endpoints
* /chars/sp/<species>/st/<status>/o/<origin> | methods=["GET"]

example:
`http://0.0.0.0:8000/chars/sp/Human/st/Alive/o/Earth`

* /healthcheck
* /environment

### deploy to k8s
#### yamls
If you need kubernetes yamls you can generate them using helm template command:

`helm template rickandmorty ./helm/rickandmorty`

#### helm
helm install rickandmorty ./helm/rickandmorty --set service.type=NodePort --set ingress.enabled=false

To use with ingress:

`minikube addons enable ingress`

`helm install rickandmorty ./helm/rickandmorty`


### Git Actions
Currently only 1 workflow with 1 job - test:
.github/workflows/main.yml

#### Steps
1. checkout the repo
2. setup minikube - uses external gh action https://github.com/marketplace/actions/setup-minikube-kubernetes-cluster
3. enable nginx ingress controller - configs a vm driver so we can enable nginx ingress for our minikube cluster
4. build image, install chart - build image from docker and installs the chat on k8s
5. test service - runs simple curl test to see healthcheck passes