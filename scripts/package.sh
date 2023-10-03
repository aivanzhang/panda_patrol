python3 -m build &&
twine check dist/* &&
python3 -m twine upload --config-file .pypirc --repository pypi dist/* 