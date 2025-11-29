install:
	python -m pip install -r requirements.txt

run-full:
	set PYTHONPATH=.; python run.py "Analyze ROAS drop (full data)"

run-sample:
	set PYTHONPATH=.; python run.py "Analyze ROAS drop (sample)"

test:
	python -m pip install pytest && pytest -q

clean:
	del /Q reports\* logs\* || exit 0

.PHONY: install run-full run-sample test clean
