#!/bin/sh

git config --global user.email "circleci@blacknode.se"
git config --global user.name "CircleCI Deployment"
git checkout master
git add cv.pdf
git commit -m "PDF build \#$CIRCLECI_BUILD_NUM"
git push origin master