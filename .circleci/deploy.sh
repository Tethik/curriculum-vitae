#!/bin/sh

git config --global user.email "circleci@blacknode.se"
git config --global user.name "CircleCI Deployment"
mv cv.pdf ..
git checkout master
mv ../cv.pdf .
git add cv.pdf
git commit -m "PDF build $CIRCLE_SHA1"
git push origin master