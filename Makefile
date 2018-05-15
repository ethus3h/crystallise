packageName = crystallize

all:
	@support/prepare $(packageName) $(DESTDIR) $(prefix) $(PREFIX) $(exec_prefix) $(bindir) $(datarootdir) $(datadir) $(sysconfdir) $(sharedstatedir)
	@echo "Done preparing" $(packageName)
install:
	@support/install $(packageName) --override-data-dir=$(OVERRIDEDATADIR) $(DESTDIR) $(prefix) $(PREFIX) $(exec_prefix) $(bindir) $(datarootdir) $(datadir) $(sysconfdir) $(sharedstatedir)
	@echo "Done installing or updating" $(packageName)
noconf:
	support/install $(packageName) --skip-config-file --override-data-dir=$(OVERRIDEDATADIR) $(DESTDIR) $(prefix) $(PREFIX) $(exec_prefix) $(bindir) $(datarootdir) $(datadir) $(sysconfdir) $(sharedstatedir)
	@echo "Done installing or updating" $(packageName)
autodep:
	@support/autodep $(packageName) $(DESTDIR) $(prefix) $(PREFIX) $(exec_prefix) $(bindir) $(datarootdir) $(datadir) $(sysconfdir) $(sharedstatedir)
	@echo "Done installing or updating dependencies for" $(packageName)
test:
	@support/test $(packageName)
	@echo "Done running tests for" $(packageName)
