all:
	rubber -d document

spellcheck:
	aspell check -t document.tex

clean:
	rubber -d --clean document
	rm -rf *.aux *~ *.log *.bbl *.blg *.lol

view: all
	evince document.pdf

