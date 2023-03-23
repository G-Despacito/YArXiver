import json
from backend import app, vector_dictionary, article_cat_info
from flask import Flask, render_template, jsonify, make_response, request, url_for, flash, redirect, session
from flask_login import login_user, logout_user, login_required, current_user
from .db_models import db, User, Paper, Author, Subject, User_Tag, Arxiv_history
from .utils import import_paper_utils as util
from .utils import get_paper_utils as get_paper_util
from .utils.recommend import recommend
from sqlalchemy import desc
import datetime


@app.route('/login', methods=['GET', 'POST'])
def user_signin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({"code":400, "status": "Username doesn't exist!"})
    elif password != user.password:
        print(user.password, password)
        return jsonify({"code":400, "status": "Password error!"})
    else:
        login_user(user, remember=True)
        return jsonify({"code":200, "status": "Success!"})


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return jsonify({"code":200, "status": "Success!"})


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/check-status', methods=['GET'])
def check_current_user():
    if not current_user.is_authenticated:
        return jsonify({"username": None})
    else:
        return jsonify({"username": current_user.username})
    
    
@app.route('/signup', methods=['GET', 'POST'])
def user_signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user is None:
        """insert a new user"""
        user = User(username=username, password=password)
        db.session.add_all([user])
        db.session.commit()
        login_user(user, remember=True)
        return jsonify({"success": 0})
    else:
        return jsonify({"success": 1})


@app.route('/library', methods=['GET'])
@login_required
def library():
    username = current_user.username
    user = User.query.filter_by(username=username).first()
    papers = user.papers.all()
    data = make_response(json.dumps([paper.to_dict() for paper in papers]))

    return data


@app.route('/bib', methods=['GET', 'POST'])
@login_required
def arxiv_to_bib():
    data = request.get_json()

    url = data.get('url')
    username = current_user.username
    # url = "https://arxiv.org/abs/1805.0"

    url_info = util.url_info_extract(url)
    if url_info is None:
        jsonify({"code": 400, "status": "url error"})
    arxiv_id, org_url, pdf_url = url_info

    bib_result = util.arxiv_to_bib(arxiv_id)
    if bib_result is None:
        return jsonify({"status": "Paper doesn't exisit!"})

    return make_response(json.dumps({
        'bib': bib_result
    }))


@app.route('/get-pdf', methods=['GET', 'POST'])
@login_required
def url_to_pdf():
    data = request.get_json()
    url = data.get('url')

    # username = current_user.username

    # url = "https://arxiv.org/abs/2104.08678"
    # 'https://arxiv.org/pdf/2210.12257.pdf'

    paper_info = util.import_paper_from_arxiv_url(url)
    if paper_info is None:
        jsonify({"code": 400, "status": "url error"})
    # arxiv_id, org_url, pdf_url = url_info

    # user = User.query.filter_by(username=username).first()
    # paper = user.papers.filter_by(arxiv_id=arxiv_id).first()

    return make_response(json.dumps({
        'url': paper_info["pdf_url"],
        "title": paper_info["title"],
    }))


@app.route('/search', methods=['GET','POST'])
@login_required
def online_search_paper():
    data = request.get_json()
    url = data.get('url')
    username = current_user.username

    if "arxiv.org" in url:
        paper_infos = [util.import_paper_from_arxiv_url(url)]
    else:
        paper_infos = util.import_paper_by_title(url)

    if paper_infos is None or not paper_infos:
        return jsonify({"code": 400, "status": "Paper doesn't exisit!"})

    arxiv_id, org_url, pdf_url = util.url_info_extract(paper_infos[0]["pdf_url"])

    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    record = Arxiv_history.query.filter_by(username=username, url=org_url).first()

    if record is None:
        record = Arxiv_history(
                        username=username,
                        url=org_url, 
                        search_time=current_time,
                    )
        db.session.add_all([record])
        db.session.commit()
    else:
        record.search_time = current_time
        db.session.commit()

    return make_response(json.dumps([{
        'url': paper_info['pdf_url'],
        'title': paper_info["title"][:100],
        'abstract': paper_info["abstract"][:500],
        'year': paper_info["publish_year"], 
        'authors': paper_info["authors"],
        'subjects': paper_info["topic"],
    } for paper_info in paper_infos]))


@login_required
@app.route('/recent-papers', methods=['GET'])
def get_recent_papers():
    username = current_user.username

    records = Arxiv_history.query.filter_by(username=username).order_by(Arxiv_history.search_time.desc()).all()
    org_urls = [record.url for record in records]
    if len(org_urls) >= 5:
        org_urls = org_urls[:5]
    # org_urls = ["https://arxiv.org/abs/2210.12257", "https://arxiv.org/abs/1806.08804"]

    papers = []
    for org_url in org_urls:
        paper_info = util.import_paper_from_arxiv_url(org_url)
        paper_dict = {
            'url': paper_info["pdf_url"],
            'title': paper_info["title"][:100],
            'abstract': paper_info["abstract"][:500],
            'year': paper_info["publish_year"],
            'authors': paper_info["authors"],
            'subjects': paper_info["topic"],
        }
        papers.append(paper_dict)

    return make_response(json.dumps(papers))


@app.route('/add-paper', methods=['GET', 'POST'])
@login_required
def add_paper():
    data = request.get_json()
    url = data.get('url')

    username = current_user.username

    # user = User.query.all()
    url_info = util.url_info_extract(url)
    if url_info is None:
        return jsonify({"code": 400, "status": "url error"})
    arxiv_id, org_url, pdf_url = url_info
    user = User.query.filter_by(username=username).first()
    flag = user.papers.filter_by(arxiv_id=arxiv_id).first()

    if flag is None:

        paper = Paper.query.filter_by(arxiv_id=arxiv_id).first()
        if paper is None:
            
            paper_info = util.import_paper_from_arxiv_url(url)

            if paper_info is None:
                jsonify({"code": 400, "status": "url error"})

            paper = Paper(
                            arxiv_id=arxiv_id, 
                            pdf_url=pdf_url,
                            abstract=paper_info["abstract"][:500], 
                            year=paper_info["publish_year"], 
                            title=paper_info["title"][:100]
                        )

            """add author"""
            author_list = []
            for authorname in paper_info["authors"]:
                cur_author = Author.query.filter_by(authorname=authorname).first()
                if cur_author is None:  # new author
                    cur_author = Author(authorname = authorname)  # create a new author
                    db.session.add_all([cur_author])
                author_list.append(cur_author)
            paper.authors = author_list

            """add subject"""
            subject_list = []
            for subjectname in paper_info["topic"]:
                subjectname = subjectname[:50]
                cur_subject = Subject.query.filter_by(subjectname=subjectname).first()
                if cur_subject is None:  # new author
                    cur_subject = Subject(subjectname = subjectname)  # create a new author
                    db.session.add_all([cur_subject])
                subject_list.append(cur_subject)
            paper.subjects = subject_list

        user.papers.append(paper)  # user add new paper

        db.session.add_all([paper])
        db.session.commit()
    # print(f"Add paper {paper.title} success!")
    
    return jsonify({"code": 200, "status": "success"})


@app.route('/attach-tag', methods=['GET', 'POST'])
@login_required
def attach_tag_to_paper():
    data = request.get_json()
    tagname = data.get('tag')
    url = data.get('url')
    username = current_user.username
    # tagname = 'test'
    # url = 'https://arxiv.org/abs/2210.12374'
    arxiv_id, org_url, pdf_url = util.url_info_extract(url)

    paper = Paper.query.filter_by(arxiv_id=arxiv_id).first()
    tag = paper.user_tags.filter_by(username=username, tagname=tagname).first()

    if tag is None:
        if len(tagname) > 20:
            return jsonify({"code": 400, "status": "tag's name is too long !!!"})
        
        new_user_tag = User_Tag(username=username, tagname=tagname)
        paper.user_tags.append(new_user_tag)
        db.session.add_all([new_user_tag])
        db.session.commit()
    
        return jsonify({"code": 200, "status": "success"})   
    else:
        return jsonify({"code": 200, "status": "already exist!"})   


@app.route('/get-paper-by-year', methods=['GET', 'POST'])
@login_required
def get_paper_by_year():
    data = request.get_json()
    # username = data.get('username')
    year = data.get('year')
    username = current_user.username
    # year = 2022
    user = User.query.filter_by(username=username).first()
    papers = user.papers.filter_by(year=year).all()
    
    # papers_data = get_paper_util.return_paper_list(papers)
    # data = make_response(papers_data)
    data = make_response(json.dumps([paper.to_dict() for paper in papers]))
    return data


@app.route('/get-paper-by-author', methods=['GET', 'POST'])
@login_required
def get_paper_by_author():
    data = request.get_json()
    # username = data.get('username')
    author = data.get('author')
    username = current_user.username
    # author = 'Yilun Zhao'
    user = User.query.filter_by(username=username).first()
    papers = user.papers.join(Paper.authors).filter(Author.authorname==author).all()
    
    # papers_data = get_paper_util.return_paper_list(papers)
    # data = make_response(papers_data)
    data = make_response(json.dumps([paper.to_dict() for paper in papers]))
    return data


@app.route('/get-paper-by-tag', methods=['GET', 'POST'])
@login_required
def get_paper_by_tag():
    data = request.get_json()

    tag = data.get('tag')
    username = current_user.username
    # tag = 'test'
    user = User.query.filter_by(username=username).first()
    papers = user.papers.join(Paper.user_tags).filter(User_Tag.tagname==tag).all()

    # papers_data = get_paper_util.return_paper_list(papers)
    # data = make_response(papers_data)
    data = make_response(json.dumps([paper.to_dict() for paper in papers]))
    return data


@app.route('/get-paper-by-subject', methods=['GET', 'POST'])
@login_required
def get_paper_by_subject():
    data = request.get_json()

    subject = data.get('subject')
    username = current_user.username
    # subject = 'Computation and Language'
    user = User.query.filter_by(username=username).first()
    papers = user.papers.join(Paper.subjects).filter(Subject.subjectname==subject).all()
    
    # papers_data = get_paper_util.return_paper_list(papers)
    # data = make_response(papers_data)
    data = make_response(json.dumps([paper.to_dict() for paper in papers]))
    return data


@app.route('/get-paper-by-title', methods=['GET', 'POST'])
@login_required
def get_paper_by_title():
    data = request.get_json()

    title = data.get('title')
    username = current_user.username
    # title = 'ReasTAP'
    # get first three results
    user = User.query.filter_by(username=username).first()
    papers = user.papers.filter(Paper.title.like('%'+title+'%')).all()
    
    # papers_data = get_paper_util.return_paper_list(papers)
    # data = make_response(papers_data)
    data = make_response(json.dumps([paper.to_dict() for paper in papers]))
    return data


@app.route('/remove-paper', methods=['GET', 'POST'])
@login_required
def remove_paper():
    data = request.get_json()

    url = data.get('url')
    username = current_user.username
    # url = 'https://arxiv.org/pdf/2104.08678.pdf'
    arxiv_id, org_url, pdf_url = util.url_info_extract(url)

    user = User.query.filter_by(username=username).first()
    paper = user.papers.filter_by(arxiv_id=arxiv_id).first()

    if paper is not None:
        db.session.delete(paper)
        db.session.commit()
        return jsonify({"code": 200, "status": "success"})   
    else:
        return jsonify({"code": 200, "status": f"{paper} not exists!"})


@app.route('/remove-tag', methods=['GET', 'POST'])
@login_required
def remove_tag():
    data = request.get_json()

    tagname = data.get('tagname')
    url = data.get('url')
    username = current_user.username
    # tagname = 'test'
    # url = 'https://arxiv.org/abs/2210.12374'
    arxiv_id, org_url, pdf_url = util.url_info_extract(url)

    paper = Paper.query.filter_by(arxiv_id=arxiv_id).first()
    tag = paper.user_tags.filter_by(username=username, tagname=tagname).first()

    if tag is not None:
        db.session.delete(tag)
        db.session.commit()
        return jsonify({"code": 200, "status": "success"})   
    else:
        return jsonify({"code": 200, "status": f"{tagname} not exists!"})


@app.route('/update-tag', methods=['GET', 'POST'])
@login_required
def update_tag():
    data = request.get_json()
    prev_tagname = data.get('tagname')
    new_tagname = data.get("new_tagname")
    url = data.get('url')
    username = current_user.username
    # prev_tagname = 'test'
    # new_tagname = 'test_update_tag'
    # url = 'https://arxiv.org/abs/2210.12374'
    arxiv_id, org_url, pdf_url = util.url_info_extract(url)

    paper = Paper.query.filter_by(arxiv_id=arxiv_id).first()
    tag = paper.user_tags.filter_by(username=username, tagname=prev_tagname).first()

    if tag is not None:
        if len(new_tagname) > 20:
            return jsonify({"code": 400})
        
        tag.tagname = new_tagname
        db.session.commit()
    
        return jsonify({"code": 200, "status": "success"})   
    else:
        return jsonify({"code": 200, "status": f"{prev_tagname} not exist!"})


@app.route('/get-paper-tag', methods=['GET', 'POST'])
@login_required
def get_paper_tag():
    data = request.get_json()
    url = data.get('url')
    username = current_user.username
    arxiv_id, org_url, pdf_url = util.url_info_extract(url)

    paper = Paper.query.filter_by(arxiv_id=arxiv_id).first()
    tags = paper.user_tags.filter_by(username=username).all()

    if tags is not None:
        return jsonify({"code": 200, "status": "success", "tags": [tag.tagname for tag in tags]})   
    else:
        return jsonify({"code": 200, "status": f"{url} not exist!"})
    

# currently only return a constant list since recommendation model has not been deployed
@login_required
@app.route('/get-recommend-papers', methods=['GET', 'POST'])
def get_recommend_papers():
    data = request.get_json()
    url = data.get('url')
    # url = "https://arxiv.org/abs/2210.12257"
    
    arxiv_id, org_url, pdf_url = util.url_info_extract(url)
    recommend_papers = recommend([arxiv_id], vector_dictionary, article_cat_info)[:10]
    data = make_response(json.dumps(recommend_papers))

    return data


@login_required
@app.route('/get-all-recommend-papers', methods=['GET'])
def get_all_recommend_papers():
    username = current_user.username

    user = User.query.filter_by(username=username).first()
    papers = user.papers.all()
    arxiv_ids = [paper.arxiv_id for paper in papers]

    if len(arxiv_ids) > 0:
        recommend_papers = recommend(arxiv_ids, vector_dictionary, article_cat_info)
        # data = make_response(json.dumps([paper.to_dict() for paper in random.sample(papers, 5)]))
        data = make_response(json.dumps(recommend_papers))
    else:
        data = make_response(json.dumps([]))

    return data
