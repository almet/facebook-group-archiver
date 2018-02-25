# Facebook group exporter

This is a tool to generate an archive of a Facebook group's discussions.

A lot of people tend to use Facebook groups to exchange data. In some areas,
it's a real information source. The problem is that not everyone has/want a Facebook
account, and letting Facebook only handle this data means we can lose it at
some point.

This tool tries to solve this problem by generating an HTML website out of a
Facebook group.

## Setup

In order to use it, you need to use the [facebook-export tool](https://github.com/KyleAMathews/facebook-export) to generate a data archive.

Once the tool is installed, here is how you can generate your data:

  $ facebook-export -a key -l # list the group ids.
  $ facebook-export -a key -a groupid
  $ facebook-analyze -g groupid -s > data.json

## Generating the website
