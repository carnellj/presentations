export POSTGRES_DB=contact_db
export POSTGRES_PASSWORD=p0stgr@s
export POSTGRES_USER=postgres
export POSTGRES_PASSSWORD=p0stgr@s
export POSTGRES_HOSTNAME=contactdb

cd contact-api && docker build . -t hackathon2019/contact && cd ..
cd notifier && docker build . -t hackathon2019/notifier && cd ..
