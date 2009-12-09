# Pour deboguer:
# for i in *.rst ; do echo $i; rst2html.py $i > build/$i; done

rst2html.py index.rst > index.html
