import openai
import pickledb
from PyPDF2 import PdfReader

from download import ArxivDownloader


class ArxivSummarizer:
    def __init__(self, api_key):
        self.downloader = ArxivDownloader()
        self.summary_db = pickledb.load('summary.db', False)
        openai.api_key = api_key

    def read_article_from_pdf(self, pdf_path):
        reader = PdfReader(pdf_path)
        pages = reader.pages
        text = ""
        for page in pages:
            sub = page.extract_text()
            text += sub

        return text

    def summarize(self, article_id):
        summary = self.summary_db.get(article_id)
        if summary:
            return summary
        pdf_path = self.downloader.download_article(article_id)
        article = self.read_article_from_pdf(pdf_path)

        summary = self._summarize_with_openai(article)

        self.summary_db.set(article_id, summary)
        self.summary_db.dump()
        return summary

    def _summarize_with_openai(self, article):
        print(f'Length of article: {len(article)}')
        cutoff_limit = int(16000 * 3.7)
        article = article[:cutoff_limit]
        system_prompt = "You are an AI assistant that help people. You will receive AI related article, please think that you and I are AI researcher and provide a summary. Write a 5000-word transcript in podcast tone to include enough information. You must reply in Korean, but as for term, you can use original form."
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",
                 "content": f"Read following article and summarize in a structured format. Be polite. Please start with '이 논문은'.\nArticle: {article}"}
            ]
        )
        return completion.choices[0].message['content']
