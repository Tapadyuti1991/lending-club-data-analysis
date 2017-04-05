FROM khozzy/selenium-python-chrome

WORKDIR /src

COPY . /

RUN pip install bs4 pandas  


CMD ["python", "/src/Autologin.py"]
