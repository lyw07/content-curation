#!/bin/bash

set -e

USERNAME=$1
BRANCH=$2
BUCKET=$3
COMMIT=$4
POSTMARK_KEY=$5
POSTGRES_USER=$6
POSTGRES_DATABASE=$7
POSTGRES_PASSWORD=$8
GCLOUD_PROXY_HOSTNAME=$9
GCS_SERVICE_ACCOUNT_JSON=$10
PROJECT_ID=${11}

if [ "${12}" ]
then
    IS_PRODUCTION=true
else
    IS_PRODUCTION=false
fi

GDRIVE_SERVICE_ACCOUNT_JSON=${13}
SENTRY_DSN_KEY=${14}

RELEASENAME="${USERNAME}-${BRANCH}"
RELEASENAME_REPLACE_UNDERSCORE="${RELEASENAME//_/-}"

helm upgrade --install $RELEASENAME_REPLACE_UNDERSCORE . \
     -f values-prod-config.yaml \
     --set studioApp.imageName=gcr.io/$PROJECT_ID/learningequality-studio-app:$COMMIT \
     --set studioNginx.imageName=gcr.io/$PROJECT_ID/learningequality-studio-nginx:$COMMIT \
     --set studioApp.releaseCommit=$COMMIT \
     --set bucketName=$BUCKET \
     --set studioApp.postmarkApiKey=$POSTMARK_KEY \
     --set postgresql.postgresUser=$POSTGRES_USER \
     --set postgresql.postgresDatabase=$POSTGRES_DATABASE \
     --set postgresql.postgresPassword=$POSTGRES_PASSWORD \
     --set postgresql.externalCloudSQL.proxyHostName=$GCLOUD_PROXY_HOSTNAME \
     --set minio.externalGoogleCloudStorage.gcsKeyJson=$(base64 $GCS_SERVICE_ACCOUNT_JSON --wrap=0) \
     --set productionIngress=$IS_PRODUCTION \
     --set studioApp.gDrive.keyJson=$(base64 $GDRIVE_SERVICE_ACCOUNT_JSON  --wrap=0) \
     --set sentry.dsnKey=$(echo "$SENTRY_DSN_KEY" | base64 --wrap=0)
