# 👮‍♂️Saies-Man AI Development 

Saies-Man은 펀드 상품 판매자에게 **상품 계약 과정에서 불완전판매 진단 서비스를 사용하여 불완전판매 발생 가능성 최소화**하는 서비스입니다.

> 불완전판매란?
> 
> 보험이나 펀드와 같은 금융상품 및 서비스 구매를 권유하는 판매자가 구매자인 고객에게 구매에 있어서 필요하고도 충분한 정보를 제공하지 않으면서, 무리한 구매나 투자권유를 하여 보험 혹은 펀드를 판매하는 행위를 총칭하는 개념

<img src="https://github.com/user-attachments/assets/bff11fdc-3c2e-48f4-913e-9fe04e0db5b0" width="900" height="350" />

## 진단 모델 플로우

GEMINI와 BERT를 이용한 불완전 판매 유형 식별 과정

<img src="https://github.com/user-attachments/assets/f203e99f-b749-43f8-974f-ed792536898d" width="900" height="350" />

## 📢 주요 기능
*(각 파트에 gif 추가)*

✅ 판매원 정보 입력  

![1](https://github.com/user-attachments/assets/d07ac2df-644a-4803-a4e2-6747f94b6328)

✅ 고객 프로필 정보 입력

![2](https://github.com/user-attachments/assets/73aaf4a1-9c3d-4b44-b497-f800ced48b86)

✅상품 선택 및 상담 내용 업로드

![3](https://github.com/user-attachments/assets/12ce7207-75fc-407e-ae07-9ed8e6d0d1c8)


✅ 진단 결과 예시

![4](https://github.com/user-attachments/assets/a6db860b-9a58-4174-bfa5-1b73b5452e3c)



---
## 📝 Description

### Data Source
*(수정 필요)*

- 간이 투자계약서  
  - 국민은행
  - 키움증권
 
- 상담 시나리오 
  


### Prerequisite 
*(수정 필요)*

```
seaborn
pandas
scikit-learn

pymysql
mysqlclient
sqlalchemy

requests
tensorflow
wordcloud
tqdm
tokenizers
sentencepiece
focal_loss
```

### Usage

```
$ streamlit run run.py
```
