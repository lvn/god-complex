# God Complex

> However, we will need to increase the modularity of our systems by encapsulating, or “hiding,” parts of the earth.

--- [King James Programming](http://kingjamesprogramming.tumblr.com/post/78840755845/however-we-will-need-to-increase-the-modularity)

In the most ambitious vision, God Complex is a toolkit for *programmatic worldbuilding* -- this is not just the procedural generation of things like terrain and room layouts, but also higher-level concepts such as civilizations, languages, and economies.

It currently generates worlds like this:

![Crappy pseudo-DF map](https://i.imgur.com/yBzxml7.png)

## Quickstart
`godcomplex` uses SQLite3 as a store for non-map persistent state. There is an SQLite database located at the root (`worldgen.db`) that contains the data used for testing.

 An extremely basic usage example is as follows.

```python
from godcomplex import World
import sqlite3

db = sqlite3.connect('file:worldgen.db?mode=ro', uri=True)
world = World(db=db)
world.init_all()

world.step()
print(world.history.events)
```

Run the `basic_test.py` script to get a more in-depth feel for how it works.

## Codebase guide
This section outlines the various components and subprojects in the repo.

* `godcomplex` is the core library with the world generation logic, exposed through the `World` class.
* `sabbath` is an experimental server that provies a RESTful (and eventually, WebSocket-based) API for world data.
* `yggdrasil` is the binary data format for persisting world map layer data.
