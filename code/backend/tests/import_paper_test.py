import pytest
from backend.utils.import_paper_utils import *

def test_url_info_extract():
    abs_url = "https://arxiv.org/abs/2210.12374"
    pdf_url = "https://arxiv.org/pdf/2210.12374.pdf"
    not_valid_url = "https://ieeexplore.ieee.org/document/9054698"
    assert url_info_extract(abs_url) == ("2210.12374", abs_url, pdf_url)
    assert url_info_extract(pdf_url) == ("2210.12374", abs_url, pdf_url)
    assert url_info_extract(not_valid_url) == None


def test_import_paper_from_arxiv_url():
    paper_info = import_paper_from_arxiv_url("https://arxiv.org/abs/2210.12374")
    assert paper_info['title'] == "ReasTAP: Injecting Table Reasoning Skills During Pre-training via Synthetic Reasoning Examples"
    assert paper_info['authors'] == ['Yilun Zhao', 'Linyong Nan', 'Zhenting Qi', 'Rui Zhang', 'Dragomir Radev']
    assert paper_info['abstract'].startswith("Reasoning over tabular data ")
    assert paper_info['pdf_url'] == "https://arxiv.org/pdf/2210.12374.pdf"
    assert paper_info['publish_year'] == 2022
    assert 'Computation and Language' in paper_info['topic']

def test_import_paper_by_title():
    paper_info = import_paper_by_title("ReasTAP")
    assert paper_info['title'] == "ReasTAP: Injecting Table Reasoning Skills During Pre-training via Synthetic Reasoning Examples"
    assert paper_info['authors'] == ['Yilun Zhao', 'Linyong Nan', 'Zhenting Qi', 'Rui Zhang', 'Dragomir Radev']
    assert paper_info['abstract'].startswith("Reasoning over tabular data ")
    
    paper_id = url_info_extract(paper_info['pdf_url'])[0]
    assert "2210.12374" in paper_id
    assert paper_info['publish_year'] == 2022
    assert 'Computation and Language' in paper_info['topic']

def test_arxiv_to_bib():
    bib = arxiv_to_bib("2210.12374")
    assert bib.startswith("@article{2210.12374")
    assert "Reasoning over tabular data" in bib
    assert "Yilun Zhao" in bib
    assert "Linyong Nan" in bib
    assert "Zhenting Qi" in bib
    assert "Rui Zhang" in bib
    assert "Dragomir Radev" in bib
