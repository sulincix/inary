PREFIX=/
all: build install

clean:
	`find | grep pycache | sed 's/^/rm -rf /g'`
	rm -rf build
build:
	python3 setup.py build
install:
	python3 setup.py install 
	ln -s /usr/bin/inary-cli /usr/bin/inary || true
	install shell-complete/bash-complete.sh /usr/share/bash-completion/completions/inary
