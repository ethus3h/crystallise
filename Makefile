all:
	@support/prepare $(DESTDIR) $(prefix) $(PREFIX) $(exec_prefix) $(bindir) $(datarootdir) $(datadir) $(sysconfdir) $(sharedstatedir)
	@echo "Done preparing crystallize"
install:
	@support/install $(DESTDIR) $(prefix) $(PREFIX) $(exec_prefix) $(bindir) $(datarootdir) $(datadir) $(sysconfdir) $(sharedstatedir)
	@echo "Done installing or updating crystallize"
noconf:
	@support/install --skip-config-file $(DESTDIR) $(prefix) $(PREFIX) $(exec_prefix) $(bindir) $(datarootdir) $(datadir) $(sysconfdir) $(sharedstatedir)
	@echo "Done installing or updating crystallize"
autodep:
	@support/autodep $(DESTDIR) $(prefix) $(PREFIX) $(exec_prefix) $(bindir) $(datarootdir) $(datadir) $(sysconfdir) $(sharedstatedir)
	@echo "Done installing or updating dependencies"
