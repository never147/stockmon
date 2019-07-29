###### Stockmon : Stock monitoring app exercise

To create a virtual env and run lint tests run:

    make dev

To create the docker image run:

    make build
    
By default the image is uploaded to the image on docker hub never147/stockmon.
You can change this by running:

    make build DOCKER_TAG='myrepo/stockmon'
  
Then update the deployment.yaml file in the k8s directory.
    
To create k8s deployment, service and associated configmap and secrets, run:

    echo "The api key" >api_key.txt
    make k8s
    
The default make target will do all of the above, additionally uploading the image to docker hub.
