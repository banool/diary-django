# Django Diary
This is an exact replica of the diary from my ftp webspace using Django. The link format is the same, the markdown is rendered into HTML in the exact same way, and the index looks exactly the same.

I don't intend for anyone else to use this, it's got too many weird little details specific to my set up.

## How does this work?
This repo is a secretless django server that exists to serve the diary. It does not contain any diary data. The backing store for the data is the [original diary](https://github.com/banool/diary). In the original repo, I would run a script that converted the markdown into HTML and then copy it across to an FTP server.

This repo contains the old repo as a submodule. Instead of converting the markdown to HTML in advance, we load the markdown into a DB and then serve it up as HTML on demand. So in this version, the true backing store for each entry is still those markdown files. This means the DB is also sort of stateless, since the data can always be loaded back up from the original diary's repo.

## Development
```
pipenv --python 3.7
pipenv install
pipenv run ./run.sh 6000
```

## Production
You need a `.env` file that contains the following keys:

- ALLOWED_HOSTS
- DB_NAME
- DB_USER
- DB_PASSWORD
- DB_HOST
- DB_PORT
- SECRET_KEY
- UI_EMAIL
- UI_USERNAME
- UI_PASSWORD

```
docker build . -t diary
docker run -p 6000:6000 --env-file .env -it diary --name diary
```

## Real production
Go use the ansible setup in [server-setup](https://github.com/banool/server-setup).


## How to setup (old)
1. Clone this repo and the [original diary](https://github.com/banool/diary).
2. `cd` into the directory for this repo and run `ln -s ~/diary/scripts/prefilter.py && ln -s ~/diary/scripts/filter.py`.
3. Make a virtualenv from the requirements file. In `bin/activate`, add a line like `export DJANGO_SETTINGS_MODULE="diary.settings.settings_prod"` to tell Django which settings file to use.

This will work fine in dev, but in prod you're going to struggle. Luckily I've figured it all out more or less, check `diary.sh` in `https://github.com/banool/server-setup` for how to set it all up properly in production.

In the original diary (probably `~/diary`) make a file called `.git/hooks/post-merge`:

```
#!/bin/bash

cd /var/www/diary-django
source myvenv/bin/activate
python manage.py shell -c "from viewer import util; util.load_new_entries()"
deactivate
```

This will get the Django diary to pull new entries in following a `git pull` in the original diary that changes something. So make sure to also put `cd ~/diary && git pull` in the crontab. This of course means that you need to push entries to the original diary repo for it to be updated on to the website.

## To do
- Tests, my previous diary was sorely lacking this.
    - Make sure that the HTML renders properly.
    - Make sure that the secret tags are respected (**important**).
    - More Django'y tests.
- Put the old diary and the new diary together. This will remove the need for symlinks into the other diary and hopefully reduce the cruft around having a hardcoded absolute path to the entry directory.
- ~Productionise the code.~
- ~Consider password protecting some / all of the diary.~
- ~Consider where to store the entries and how to let Django know of their location. Where is the best place to store this piece of config information? What about in production?~ Currently it still needs to refer to the old diary scripts.

