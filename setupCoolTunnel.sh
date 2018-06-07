wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-204.0.0-linux-x86_64.tar.gz
tar zxvf google-cloud-sdk-204.0.0-linux-x86_64.tar.gz
./google-cloud-sdk/install.sh
./google-cloud-sdk/bin/gcloud init
./google-cloud-sdk/bin/gcloud compute ssh --zone us-west1-b instance-1 -- -N -R8080:localhost:5000
