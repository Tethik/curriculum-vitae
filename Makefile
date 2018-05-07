filename=cv

pdf: # build twice, because latex.
	xelatex ${filename} && xelatex ${filename}

clean:
	rm -f ${filename}.{ps,pdf,log,aux,out,dvi,bbl,blg,snm,toc,nav}
