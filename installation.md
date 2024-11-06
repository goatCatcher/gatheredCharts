To install this project, you need to have Python 3.6 or higher installed on your machine. You can download the latest version of Python from the official website. After installing Python, you can install the required dependencies using the following command:

```bash
# Run command 1
pip install poetry

# Run command 2
poetry config virtualenvs.in-project true
poetry install

poetry self add "poetry-dynamic-versioning[plugin]"

# Install pre-commit hooks
pre-commit install
```
