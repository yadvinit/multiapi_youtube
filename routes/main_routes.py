from flask import Blueprint, render_template, request, current_app, jsonify
from services.youtube_service import get_recent_videos

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    query = request.args.get('q', current_app.config['DEFAULT_SEARCH_QUERY'])
    page = request.args.get('page', 1, type=int)
    
    result = get_recent_videos(query, page=page, per_page=current_app.config['RESULTS_PER_PAGE'])
    
    if 'error' in result:
        return render_template('home.html', 
                              query=query,
                              error=result['error'])
    
    return render_template('home.html',
                          query=query,
                          videos=result['videos'],
                          page=result['page'],
                          has_next=result.get('has_next', False),
                          has_prev=result.get('has_prev', False),
                          next_page=result.get('next_page'),
                          prev_page=result.get('prev_page'),
                          is_cached=result.get('cached', False))

@main_bp.route('/api')
def api():
    query = request.args.get('q', current_app.config['DEFAULT_SEARCH_QUERY'])
    page = request.args.get('page', 1, type=int)
    
    result = get_recent_videos(query, page=page, per_page=current_app.config['RESULTS_PER_PAGE'])
    
    if 'error' in result:
        return jsonify({'error': result['error']}), 500
    
    return jsonify({
        'query': query,
        'videos': result['videos'],
        'pagination': {
            'page': result.get('page', 1),
            'total_results': result.get('total', 0),
            'has_next_page': result.get('has_next', False),
            'has_prev_page': result.get('has_prev', False),
            'next_page': result.get('next_page'),
            'prev_page': result.get('prev_page')
        },
        'from_cache': result.get('cached', False)
    })

