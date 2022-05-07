clean:
	rm *.png *.json *.dot

dependencies:
	pip install matplotlib networkx pydot

example1:
	python3 full_assignment.py "(XB|C[A-Z])+"

example2:
	python3 full_assignment.py "a*(a|b)aa"

example3:
	python3 full_assignment.py "0|1(0|1)*00"