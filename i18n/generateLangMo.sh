rm en_US/LC_MESSAGES/*.mo 
rm it_IT/LC_MESSAGES/*.mo

msgfmt --output-file=en_US/LC_MESSAGES/photoOrganizer.mo en_US.po
msgfmt --output-file=it_IT/LC_MESSAGES/photoOrganizer.mo it.po
