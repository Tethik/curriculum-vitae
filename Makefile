filename=cv

pdf: # build twice, because latex typically needs two runs to fix the images and links. It's weird.
	xelatex ${filename} && xelatex ${filename}

clean:
	rm -f ${filename}.{ps,pdf,log,aux,out,dvi,bbl,blg,snm,toc,nav}
