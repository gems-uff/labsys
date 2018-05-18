from flask import current_app, request, url_for, render_template


def get_page_size():
    return current_app.config['PAGE_SIZE']


def get_page():
    return request.args.get('page', 1, type=int)


def paginated(query, template_name, view_method, context_title):
    page = get_page()
    page_size = get_page_size()
    query = query.paginate(page, page_size, False)
    prev_url = url_for(
        view_method, page=query.prev_num) if query.has_prev else None
    next_url = url_for(
        view_method, page=query.next_num) if query.has_next else None
    context = {
        context_title: query.items,
    }
    return render_template(template_name,
                           **context,
                           next_url=next_url,
                           prev_url=prev_url)
