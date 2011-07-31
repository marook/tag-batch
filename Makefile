
install: ~/.local/bin/tag_batch.py

~/.local/bin/tag_batch.py: tag_batch.py
	cp -a "$^" "$@"
