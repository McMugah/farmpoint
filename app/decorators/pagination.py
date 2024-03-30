import functools
from flask import url_for, request

def paginate(collection, max_per_page=25):
    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            # Ensure the query object is retrieved correctly
            query = f(*args, **kwargs)

            # Check if the query object is None or empty
            if query is None:
                return {"error": "Query object is None"}

            # Ensure the query object has the paginate method
            if not hasattr(query, 'paginate'):
                return {"error": "Query object does not have paginate method"}

            # Retrieve pagination parameters from request
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', max_per_page, type=int), max_per_page)
            expanded = request.args.get('expanded', 'false').lower() in ['true', '1']

            # Perform pagination
            p = query.paginate(page, per_page)
            pages = {'page': page, 'per_page': per_page, 'total': p.total, 'pages': p.pages}

            # Construct pagination URLs
            if p.has_prev:
                pages['prev_url'] = url_for(request.endpoint, page=p.prev_num, per_page=per_page, expanded=expanded, **kwargs)
            else:
                pages['prev_url'] = None

            if p.has_next:
                pages['next_url'] = url_for(request.endpoint, page=p.next_num, per_page=per_page, expanded=expanded, **kwargs)
            else:
                pages['next_url'] = None

            pages['first_url'] = url_for(request.endpoint, page=1, per_page=per_page, expanded=expanded, **kwargs)
            pages['last_url'] = url_for(request.endpoint, page=p.pages, per_page=per_page, expanded=expanded, **kwargs)

            # Retrieve results based on pagination settings
            if expanded:
                results = [item.export_data() for item in p.items]
            else:
                results = [item.get_url() for item in p.items]

            return {collection: results, 'pages': pages}
        return wrapped
    return decorator
