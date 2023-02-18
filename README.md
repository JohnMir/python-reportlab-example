# python-reportlab-example
PDF Report example with a front-page, header, footer and table

#___

# TODO
## Color terminal
## 

https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QLabel.html

# Workflow
drag.py gets filenames
create.py creates pdf with images on each page

# Executable installer
Install pyinstaller: 
```
pip install pyinstaller
pip install reportlab
pip install PyQt5
```

Create executable:
```
pyinstaller --onefile dragtest.py
```



```python
if __name__ == '__main__':
    report = PDFPSReporte('psreport234.pdf')
```