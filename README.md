# shepherd-2

A rewrite of shepherd using python 3.10 and FastAPI.

Reasons for a re-write:
 1. 1.0 was designed to serve webpages we now use shepherd as an API. This fundemental different use means that large sections of the code are now obsolete and there is clutter and assumptions based on how things used to be
 2. There are features like doing images via a socket and the current design isn't too extensible
 3. It is possible to crash shepherd from usercode. Some of these bugs are quite deep in shepherd.
 5. Cleaning up shepherd and re-factoring is probally about as much work as just re-writing it now we know what we want.
 6. The calling convention for the robot lib are *weird* this alone is not a bad thing but it does make maintance harder.
 7. It is not clear what is meant to be in the API and what is just hacked functionality
 8. There is no unit testing

Reasons against the re-write:
 1. Shepherd 1.0 has been extensively battle tested
 2. A re-write might be a waste of developement effort
 3. All of the problems can be solved with a refactor

I (Edwin) think that a prototype re-write should at least be tried to see how hard it is mainly for 2, 6 and 7.

Additionally there are a whole load of features which a new shepherd could support but for now we just need to focus on feature parity.

## Getting started

Dependencies are managed using poetry which you can get
[here](https://python-poetry.org/docs/master/#installing-with-the-official-installer)

```
poetry install
```

This will create a virtual environment where the dependencies will be installed
this means that they will only be available for shepherd and will not interfere
with the rest of your system.

You can enter this virtual environment by:

```
poetry shell
```

Start the server in development mode (hot reload)
```
dev = "poetry run uvicorn app:app --reload"
```

Run tests
```
pytest -x
```

## Documentation

Documentation is available for this project here: TODO
