# Facebook group archiver

This is a tool to generate an archive of a Facebook group's discussions.

A lot of people tend to use Facebook groups to exchange data. In some areas,
it's a real information source. The problem is that not everyone has/want a Facebook
account, and letting Facebook only handle this data means we can lose it at
some point.

This tool tries to solve this problem by generating an HTML website out of a
Facebook group.

**Unfortunately, you currently need to be an administrator of the group to
run this archiver**. I believe this is how Facebook does data retention :/

## Dependencies

To access your data through the Facebook API, Facebook requires you to use an access token. This must be included when you run facebook-export. You can get one at https://developers.facebook.com/tools/explorer. Be sure to check "user_groups". [More information on how to setup this is available here](https://github.com/KyleAMathews/facebook-export#export-data-from-facebook).

```bash
npm install -g facebook-export
facebook-export -a key -l # list the group ids.
facebook-export -a key -a groupid
facebook-analyze -g groupid -s > data.json
```
## Setup

You need to install this. After checking-out the code, you need to install
it in a virtual environment:

```bash
virtualenv .venv
.venv/bin/pip install -r requirements.txt
```

## Generating the website

Once everything is done, you can generate the website using::

```bash
.venv/bin/python scrap.py --output output --data content/data.json
```
