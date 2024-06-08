# clap-caption

The clap-caption is a minimal tool for caption sounds by [msclap](https://github.com/microsoft/CLAP)


## Installation

1. Clone repository
   ```bash
   git clone https://github.com/TylorShine/clap-caption
   cd clap-caption
   ```

1. (Optional but recommended) Create and activate your Python environment
   ```bash
   # for example, we use venv
   python -m venv venv
   ```

1. Install dependencies using pip
   ```bash
   pip install -r requirements.txt
   ```


## Usage

```bash
python clap-caption.py <your audio file(s)... or folder(s) include audio file(s)...>
```
This outputs JSON Line file.  
For more options, `python clap-caption.py -h`


## License

[CC0](https://creativecommons.org/publicdomain/zero/1.0/)


## Acknowledgements

- [CLAP](https://github.com/microsoft/CLAP)
