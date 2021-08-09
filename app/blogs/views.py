from . import blogs


@blogs.route('/', default={'page_idx':1})
@blogs.route('/page/<int:page_idx>', methods=['GET'])
def index(page_idx):
     pass
