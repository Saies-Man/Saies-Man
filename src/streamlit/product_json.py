import os
import json
import pandas as pd 
import streamlit as st
class JSONFileManager:
    def __init__(self, directory):
        self.directory = directory
        self.df = self.create_file_df()
        self.json_content = ""  # JSON 파일의 내용을 저장할 변수

    def create_file_df(self):
        data = []
        for filename in os.listdir(self.directory):
            if filename.endswith('.json'):
                name = filename.split('.')[0]  # 확장자 제외한 파일 이름
                data.append({"name": name})
        return pd.DataFrame(data)

    def display_product_names(self):
        # 사용 가능한 JSON 파일 목록을 출력
        print("Available JSON Files:")
        for idx, name in enumerate(self.df['name'], start=1):
            print(f"{idx}. {name}")

    def read_json_as_text(self, product_name):
        file_path = os.path.join(self.directory, product_name + '.json')
        if not os.path.exists(file_path):
            st.error("Error: File does not exist.")
            return "Error: File does not exist."  # 파일이 없으면 에러 메시지 반환

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.json_content = file.read()
                st.text_area("JSON 파일 내용", self.json_content, height=300)  # Streamlit을 사용하여 내용 표시 나중에 삭제할 것 
                return self.json_content
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return ""
    # def read_json_as_text(self, product_name):
    #     file_path = os.path.join(self.directory, product_name + '.json')
    #     try:
    #         with open(file_path, 'r', encoding='utf-8') as file:
    #             self.json_content = file.read()
    #             print(self.json_content)  # 출력
    #     except Exception as e:
    #         print(f"An error occurred: {e}")

    def find_and_display_product(self):
        self.display_product_names()
        try:
            choice = int(input("Enter the number of the product to load its JSON file: "))
            product_name = self.df.iloc[choice-1]['name']
            self.read_json_as_text(product_name)
        except IndexError:
            print("Invalid selection. Please enter a valid number.")
        except ValueError:
            print("Please enter a numerical value.")

    def get_json_content(self):
        # JSON 내용을 반환하는 메서드
        return self.json_content

