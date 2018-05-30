import os

from collections import defaultdict

from flask import render_template, flash, redirect, url_for, request
from flask import current_app, send_from_directory

from app.models import Picture
from app.main import bp

@bp.route('/')
@bp.route('/index')
def index():
    """
    main page of the blog:
    it shows 5pages carousel
    10 photos ordered by shot time per page
    """
    pictures = Picture.objects().order_by('-shot_time')
    carousel_pictures = pictures.order_by('-create_time')[:5]
    page = request.args.get('page', 1, type=int)
    paginated_pictures = pictures.paginate(page=page,
                                           per_page=current_app.config['PIC_PER_PAGE'])
    current_page = paginated_pictures.page
    total_page = paginated_pictures.pages
    next_url = url_for('main.index', page=paginated_pictures.next_num) \
                        if paginated_pictures.has_next else None
    prev_url = url_for('main.index', page=paginated_pictures.prev_num) \
                        if paginated_pictures.has_prev else None
    url_list = []
    for p in range(1, total_page+1): # so page number start from 1
        url = url_for('main.index', page=p)
        url_list.append(url)
    return render_template('main/index.html',
                           pictures=paginated_pictures.items,
                           next_url=next_url,
                           prev_url=prev_url,
                           carousel_pictures=carousel_pictures,
                           current_page=current_page,
                           total_page=total_page,
                           url_list=url_list)

@bp.route('/about')
def about():
    """
    about page
    a static page shows info about the site
    """
    pictures = Picture.objects()
    carousel_pictures = pictures.order_by('-create_time')[:5]
    return render_template('main/about.html', carousel_pictures=carousel_pictures)

@bp.route('/pictures_by_year')
def pictures_by_year():
    """
    view photos by year
    """
    pictures = Picture.objects().order_by('-shot_time')
    year = 0
    years = []
    pictures_by_year = defaultdict(list)
    for picture in pictures:
        year = picture.shot_time.year
        if year not in years:
            years.append(year)
        pictures_by_year[year].append(picture)
    return render_template('main/pictures_by_year.html',
                           pictures_by_year=pictures_by_year,
                           years=years)

@bp.route('/pictures_by_tag/<tag>')
def pictures_by_tag(tag):
    """
    view photos by tag
    """
    pictures = Picture.objects(tags=tag).order_by('-shot_time')
    tag_dict = {
    'mountain': '高山',
    'water': '流水',
    'things': '万物',
    'people': '人间',
    'me': '我',
    }
    return render_template('main/pictures_by_tag.html',
                           pictures=pictures,
                           tag=tag,
                           tag_dict=tag_dict)

@bp.route('/static/pictures/<path:filename>')
def serve_pictures(filename):
    return send_from_directory(os.path.join(current_app.config['APP_DIR'], current_app.config['UPLOAD_FOLDER']), filename)

@bp.route('/static/<path:filename>')
def serve_static_files(filename):
    return send_from_directory(os.path.join(current_app.config['APP_DIR'], current_app.config['STATIC']), filename)
