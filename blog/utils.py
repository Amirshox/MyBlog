def get_children(qs_child):
    res = []
    for comment in qs_child:
        c = {
            'id': comment.id,
            'body': comment.body,
            'created': comment.created,
            'updated': comment.updated,
            'author': comment.user,
            'is_child': comment.is_child,
            'parent_id': comment.parent_id
        }
        if comment.comment_children.exists():
            c['children'] = get_children(comment.comment_children.all())
        res.append(c)
    return res


def create_comments_tree(qs):
    res = []
    for comment in qs:
        c = {
            'id': comment.id,
            'body': comment.body,
            'created': comment.created,
            'updated': comment.updated,
            'author': comment.user,
            'is_child': comment.is_child,
            'parent_id': comment.parent_id
        }
        if comment.comment_children:
            c['children'] = get_children(comment.comment_children.all())
        if not comment.is_child:
            res.append(c)
    return res
