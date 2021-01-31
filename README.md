# Stock prediction by machine learning

### Project Description

과거 주가정보를 바탕으로 기계학습 기법을 이용해 미래 주가를 예측하는 모델생성

유의미한 결과가 나올때 까지 알고리즘들을 업로드할 예정입니다.

### Data Source

KRX(한국거래소)

### ipynb files

- stock_get_data.ipynb 

  ```
  Get data using finance data reader library
  - 주가 정보 using fdr
  - 거래주체(기관, 외인) from krx
  - 재무제표 from naver finance
  ```

- prediction_LSTM.ipynb

  ```
  Predict next day stock price by LSTM
  간단한 LSTM모형을 이용해 주가예측 - fail
  ```

- prediction_clustering.ipynb 

  ```
  Predict next day stock price using clustering, DNN
  최근 주가의 흐름을 clustering을 이용해 분류 후 다음날 주가횡보 예측 - ?
  시가, 종가, 고가, 거래량 등을 변수로 다음날 주가횡보 예측 - fail
  ```

- trade_who_price.ipynb

  ```
  Predict using foreign and institution's trading data
  기관, 외인들의 순매매량 데이터를 이용해 다음날 주가횡보 예측 - ?
  ```

- new_high.ipynb

  ```
  Predict using 'new high price for specific term'
  특정기간동안(ex 1년) 신고가 경신한 종목의 횡보
  ```

  