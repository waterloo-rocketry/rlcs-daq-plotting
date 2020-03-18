# python venv (gitbash on windows syntax)
## Installing from requirements
* >python -m venv venv
* >source venv/Scripts/activate
* >pip install -r requirements.txt

## Updating requirements
* >source venv/Scripts/activate
* >pip freeze >requirements.txt

# TODO
* figure out how to limit axis max length now that we use extendData
* make the adjusted value pop out more than the others
* find a way to use relative timestamps on the frontend only by manually generating ticks
