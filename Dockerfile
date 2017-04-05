#FROM danielfrg/selenium

#### REF: http://blog.likewise.org/2015/01/setting-up-chromedriver-and-the-selenium-webdriver-python-bindings-on-ubuntu-14-dot-04/

#FROM PYTHON

FROM khozzy/selenium-python-chrome

RUN pip install --upgrade pip

RUN pip install bs4 pandas unzip 


ARG LATEST=$(wget -q -O - http://chromedriver.storage.googleapis.com/LATEST_RELEASE)
#ENV LATEST=${LATEST}

RUN wget http://chromedriver.storage.googleapis.com/$LATEST/chromedriver_linux64.zip

RUN unzip chromedriver_linux64.zip && sudo ln -s $PWD/chromedriver /usr/local/bin/chromedriver
WORKDIR /src

COPY . /src

#RUN git clone https://github.com/jainpranj/lending-club-data-analysis.git /src

CMD ["python", "/src/Autologin_and_download.py"]
