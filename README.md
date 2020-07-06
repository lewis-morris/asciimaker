ASCII Maker
------------

### Installation


```commandline
pip install asciimaker
```

or if you dont have pip

```commandline
git clone "https://github.com/lewis-morris/asciimaker" && cd asciimaker && python setup.py install
```


### Usage
First import AsciiMaker

```python
import AsciiMaker
```

Then start using

```python
asc = AsciiMaker.Maker(w_size=800, block_size=5, invert=False, colour=True, characters="8@%#")
asc.write_html("dog.jpg", "dog.html")
```

![doggo](examples/dog.png "Dog")

