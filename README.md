# Common Code Kevin uses
Common code Kevin uses

## To add

```bash
git submodule add git@github.com:ICRAR/common-kv.git common-kv
git submodule update --init
```
Or when cloning

```bash
git clone https://github.com/aikiframework/json.git --recursive
```

## To Install

```bash
cd <blah>/common-kv
pip install -e .
```

The _-e_ option stands for editable, which is important because it allows you to change the source code of your package without reinstalling it.