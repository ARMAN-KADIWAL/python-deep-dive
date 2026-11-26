# Lab 95 — Enhanced Python REPL

Practice in a real interactive Python 3.13 terminal. No external packages required.

1. Run `python3.13 --version` and `python3.13`.
2. Try multiline functions, dictionaries and strings; Up/Down and Ctrl+R search; F1 help, F2 history, F3 paste mode.
3. Observe deliberate SyntaxError, ZeroDivisionError and TypeError.
4. History browsing uses F2; CPython does not provide the lab's proposed built-in history() function. For file export in PyREPL 3.13, `import _pyrepl.readline as rl; rl.write_history_file("my_session.hist")` uses a private implementation API. The basic REPL uses the public readline module. Never publish personal command history.
5. Practice pdb commands n, s, p, pp, c and q. Load examples with `python3.13 -i repl_examples.py` and call `pdb.runcall(factorial_bug, 5)` to inspect the missing final iteration. Call `analyze_data([5,15,8,22,3,18,12,7,25,11], debug=True)` and step through the local variables.
6. Verify with `python3.13 -m unittest -v`.

Keyboard-driven terminal tasks and intentional errors must be demonstrated interactively; unit tests do not replace those exercises.

Reference: https://docs.python.org/3.13/tutorial/appendix.html
