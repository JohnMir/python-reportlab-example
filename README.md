# python-reportlab-example
PDF Report example with a front-page, header, footer and table

#___

# TODO
## Color terminal
## 

# Workflow
drag.py gets filenames
create.py creates pdf with images on each page

# Executable installer
Install pyinstaller: 
```
pip install pyinstaller
```

Create executable:
```
pyinstaller --onefile yourscriptname.py
```



```python
if __name__ == '__main__':
    report = PDFPSReporte('psreport234.pdf')
```