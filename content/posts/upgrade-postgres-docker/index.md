---
title: "Upgrade PostgreSQL in Docker"
date: 2023-08-17T22:52:07+02:00
draft: false
tags: ["postgres", "postgresql", "docker", "upgrade", "self-hosting", "database"]

# Keep them short
summary: "Upgrading postgresql can't be done in-place, so here's a scripted version to help you do so."

cover:
  image: "elephant.jpg"
  relative: true
  alt: "Trumpeting elephant"
  caption: "Trumpeting elephant (Muhammad Mahdi Karim, GFDL 1.2)"
  hidden: false  # applies only on single view

#showToc: true
#TocOpen: false
---

Upgrading postgresql can't be done in-place, you have to setup a new DB with the expected version and restore your content in this DB.

I had a few containers running older versions of postgres lying around (13 and 14), and I wanted to upgrade them to postgresql 15. Here's the script I came up with.

{{< note class="warning" title="⚠️ Warning" >}}
When handling production data, don't blindly run this as a script. Run each step manually and double-check that you aren't destroying anything.
{{< /note >}}

{{< note class="info" >}}
This post is inspired by [Thomas Bandt's](https://thomasbandt.com/postgres-docker-major-version-upgrade), with some tweaks in the process, and less writing.
{{< /note >}}

```bash
app_name="app"
db_user="user"
db_name="db"

# Stop the running app(s)
# to prevent modifications during the backup & restore
docker compose stop $app_name

# Dump DB & roles
# I'm using custom scripts for this part in order to run
# them regularly and export the backups.
# Here's what they basically do.
docker compose exec -it db \
  pg_dump -Fc -U $db_user $db_name > ./db_export/backup.dump
docker compose exec -it db \
  pg_dumpall --globals-only -U $db_user > ./db_export/roles.sql

# Shutdown everything
docker compose down

# Move current data dir, don't remove it yet
mv db_data db_data_OLD

# edit docker-compose.yaml - upgrade psql
vim docker-compose.yaml

# Up the new database & check version
docker compose up -d db
docker compose exec -it db psql -U $db_user -c 'select version();'

# Restore roles
# Skip for simple DB where only 1 user,
# managed by the docker image, is used
docker compose cp ./db_export/roles.sql db:/tmp/roles
docker compose exec -it db psql -U $db_user -d $db_name -f /tmp/roles

# Restore content
docker compose cp ./db_export/backup.dump db:/tmp/backup
docker compose exec -it db pg_restore -U $db_user -d $db_name /tmp/backup

# Check if content is properly restored:
# list tables, make a few queries
docker compose exec -it db psql -U $db_user -d $db_name -c "\dt"

# Launch app again
docker compose up -d
docker compose logs -ft

# check app still works and has data

# Finally remove the old data dir
rm -rf db_data_OLD
```

If your database is not in a container, then [`pg_upgrade`](https://www.postgresql.org/docs/current/pgupgrade.html) may be a better option: faster, less hassle and doesn't require manually dumping and restoring.

{{<unsafe>}}
<small>
Postgres, PostgreSQL and the Slonik Logo are trademarks or registered trademarks of the PostgreSQL Community Association of Canada, and used with their permission.
</small>
{{</unsafe>}}
