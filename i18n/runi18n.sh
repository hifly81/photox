rm photoOrganizer.pot
rm *.po
rm glade/photoOrganizerGui.glade.h

xgettext --language=Python --keyword=_ --output=photoOrganizer.pot `find . -name "*.py"`
intltool-extract --type=gettext/glade glade/photoOrganizerGui.glade
xgettext --language=Python --keyword=_ --keyword=N_ --output=photoOrganizer.pot `find . -name "*.py"` glade/photoOrganizerGui.glade.h
msginit --input=photoOrganizer.pot --locale=en_US
msginit --input=photoOrganizer.pot --locale=it_IT

