set -e

USERNAME=$1
BRANCH=$2

INSTANCE="studio-pr-demo"
DBNAME="${USERNAME}-${BRANCH}"

DATABASES=`gcloud sql databases list --instance=${INSTANCE} | awk '{print $1}' | tail -n +2`

EXISTENCE=False

for word in ${DATABASES}; do
    if [[ ${word} = ${DBNAME} ]];
    then
        echo "Database ${DBNAME} exists in SQL instance ${INSTANCE}."
        EXISTENCE=True
        break
    fi
done


if [[ ${EXISTENCE} = False ]];
then
    echo "Creating database ${DBNAME} in SQL instance ${INSTANCE}."
    gcloud sql databases create ${DBNAME} --instance=${INSTANCE}
fi
