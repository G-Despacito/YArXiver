import json

def return_paper_list(papers):
    output_data = json.dumps({
        'url': [paper.url for paper in papers],
        'title': [paper.title for paper in papers],
        'abstract': [paper.abstract for paper in papers],
        'year': [paper.year for paper in papers],
        'authors': [author.authorname for paper in papers for author in paper.authors.all()],
        'subjects': [subject.subjectname for paper in papers for subject in paper.subjects.all()],
        'tags': [user_tag.tagname for paper in papers for user_tag in paper.user_tags.all()],
    })
    return output_data
