# 🤖 𝕽𝖔𝖔𝖙𝕸𝖊-𝕮𝖍𝖊𝖆𝖙𝖊𝖗-𝕾𝖈𝖆𝖓𝖓𝖊𝖗
Calculate the cheat rate of one or more Root-Me players.

### ⚠️ Attention ⚠️
These statstics mean nothing if the context is not known.

## ⚙️ Installation
```bash
git clone https://github.com/Jb799/RootMe-Cheater-Scanner.git
cd RootMe-Cheater-Scanner
python(3) -m pip install -r requirements.txt
```

## 🗡️ Usage
Scan only one player:<br/>
*python or python3*
```bash
python3 main.py toto
```

Scan a list of players<br/>
*python or python3*
```bash
python3 main.py toto tata titi
```

## 🐧 For WSL
Add at the top of the main.py
```python
import matplotlib
matplotlib.use('TkAgg')
```
&
Install Lib:<br/>
*python or python3*
```bash
sudo apt-get install python3-tk
```
