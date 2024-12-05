# Comparative Analysis of Flipkart/Amazon Customer Reviews + WST

## To Run

### Firstly, in a Windows Terminal
```bash
cd .\Desktop\
git clone git@github.com:joelblr/CAAFR.git
cd .\CAAFR\
explorer .
taskmgr
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
cd .\wst_app\
npm i
cd ../
cls
python .\st_app\backend\backend.py

```
### Secondly, in another Windows Terminal
```bash
cd .\Desktop\CAAFR\
.\venv\Scripts\activate
cls
streamlit run .\st_app\frontend\0_??_Home.py

```

