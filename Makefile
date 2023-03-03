#
# Makefile
#
# CSC309 Assignment 2
#
# There is only 1 command, which deletes all
# files that you should not submit, except
# for the virtual environment (venv).
#

.PHONY: clean
clean:
	rm -rf db.sqlite3 */__pycache__
