# curriculum-vitae
CI/CD for my CV. 

The LateX in this repo gets built on CircleCI via a Docker image. The pdf is committed and pushed back into 
this repo onto the master branch, which is served by github pages. 

You can access the final result here:
https://tethik.github.io/curriculum-vitae/cv.pdf


## Building using docker
```
docker run --rm -v $(pwd):/data tethik/xelatex make
```

## Credits
- LateX template originally was taken from sharelatex.
- [This docker xelatex image](https://github.com/moss-it/docker-xelatex)