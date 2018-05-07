######################
#      Makefile      #
######################

filename=cv

pdf:
	xelatex ${filename} && xelatex ${filename}

clean:
	rm -f ${filename}.{ps,pdf,log,aux,out,dvi,bbl,blg,snm,toc,nav}
