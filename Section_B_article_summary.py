# Author: Zehao ZHANG 24069596g

from Section_B_arxiv_api_integration_ai_connect import answer
from Section_B_pdf_processing import pdf_to_txt
# 从settings.py中导入全局变量
from Section_B_settings import USER_PROMPT
import json

# 考虑PDF文件名和文章名不一致的情况
# 文件名可从用户上传的文件中读取，文章名由另一section提供
def get_context_and_feedback_from_ai(pdf_name, article_name, translation = "English"):
    try:
        pdf_to_txt(pdf_name)
        with open(f"{pdf_name}.txt", "r") as f:
            article_text = f.read()
        user_prompt = USER_PROMPT
        user_prompt = user_prompt.replace("{article_text}", article_text)
        user_prompt = user_prompt.replace("{article_name}", article_name)
        # print(user_prompt)
        
        output_information = answer(user_prompt, translation)
        output_dict = json.loads(output_information)
        # 按照段落标题来分割原文
        # 滑动空间？-未实现
        titles = []
        for key in output_dict['summaries'].keys():
            titles.append(key)
        # print(titles)
        # print("/*---------------------------------------------------------------*/")
        for title in titles:
            article_text = article_text.replace(title, "\n\n\n\n\n")
        article_text_list = article_text.split("\n\n\n\n\n")
        # print(article_text_list)
        # print("/*---------------------------------------------------------------*/")
        output_dict['text'] = dict(zip(titles, article_text_list[1:]))
        output_dict['AI_Status'] = "OK"
        #print(output_dict)
        #print("/*---------------------------------------------------------------*/")
        return output_dict
    except Exception as e:
        return {
            "AI_Status": "Error",
            "Error": str(e) + " Please contact the authors of this web application."
        }