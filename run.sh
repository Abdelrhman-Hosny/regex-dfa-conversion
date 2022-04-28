/usr/bin/python lab2.py

dot nfa.dot -Tpng > nfa.png
mimeopen nfa.png

dot dfa.dot -Tpng > dfa.png
mimeopen dfa.png

dot dfa_min.dot -Tpng > dfa_min.png
mimeopen dfa_min.png