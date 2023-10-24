import os

import arxiv


class ArxivDownloader:
    def __init__(self):
        self.pdf_dir = './pdfs'
        os.makedirs(self.pdf_dir, exist_ok=True)

    def download_article(self, article_id, pdf_path=None):
        search = arxiv.Search(id_list=[article_id])
        paper = next(search.results())
        if not pdf_path:
            pdf_path = os.path.join(self.pdf_dir, article_id + '.pdf')
        if not os.path.exists(pdf_path):
            paper.download_pdf(filename=pdf_path)
        return pdf_path

    def download_from_list(self, list_file_name='./download_list.txt'):
        with open(list_file_name) as f:
            for line in f.readlines():
                article_id = line.strip()
                pdf_path = os.path.join(self.pdf_dir, article_id + '.pdf')
                if os.path.exists(pdf_path):
                    print("Already downloaded article. Skipping download...")
                else:
                    print(f"Downloading article {article_id}...")
                    self.download_article(article_id, pdf_path)
                    print(f"Downloaded {article_id} in {pdf_path}...")


if __name__ == '__main__':
    ad = ArxivDownloader()
    ad.download_from_list()
