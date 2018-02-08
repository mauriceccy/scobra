# scobra
scobra - an extension of cobrapy with ScrumPy

## Installation 

### Windows 
1. Make sure that [python2.7](https://www.python.org/downloads/release/python-2714/), [git](https://git-scm.com/downloads) 
and [pip](https://pip.pypa.io/en/stable/installing/) are installed
2. (Optional) Create a virtual environment and activate it <br />
```
pip install virtualenv 
pip install virtualenvwrapper
virtualenv -p PATH\TO\DIRECTORY PROJECT_NAME
cd PROJECT_NAME
call Scripts\activate 
```
3. Clone scobra repository <br />
``` 
git clone https://github.com/mauriceccy/scobra.git 
```
4. Install all requirements <br />
```
FOR /F %A in (scobra\requirements.txt) do pip install %A 
```
### Mac OS
1. Make sure that python2.7, [python2.7](https://www.python.org/downloads/release/python-2714/), [git](https://git-scm.com/downloads) 
and [pip](https://pip.pypa.io/en/stable/installing/) are installed
2. (Optional) Create a virtual environment and activate it <br />
```
pip install virtualenv 
virtualenv -p /usr/bin/python2.7 PROJECT_NAME 
cd PROJECT_NAME
source bin/activate
```
3. Clone scobra repository <br />
```
git clone https://github.com/mauriceccy/scobra.git 
```

4. Install all requirements <br />
```
cat scobra/requirements.txt | xargs -I {} pip install {} 
```

### Linux
1. Make sure that python2.7, [python2.7](https://www.python.org/downloads/release/python-2714/), [git](https://git-scm.com/downloads) 
and [pip](https://pip.pypa.io/en/stable/installing/) are installed
2. (Optional) Create a virtual environment and activate it <br />
```
pip install virtualenv 
virtualenv -p /usr/bin/python2.7 PROJECT_NAME 
cd PROJECT_NAME
source bin/activate
```
3. Clone scobra repository <br />
```
git clone https://github.com/mauriceccy/scobra.git 
```
4. Install all requirements <br />
```
cat scobra/requirements.txt | xargs -I {} pip install {} 
```