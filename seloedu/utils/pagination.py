from math import ceil


class Pagination:
    def __init__(self, items, page, per_page, total):
        self.items = items
        self.page = page
        self.per_page = per_page
        self.total = total
        self.pages = max(ceil(total / per_page), 1)
        self.has_prev = page > 1
        self.has_next = page < self.pages
        self.prev_num = page - 1
        self.next_num = page + 1


def paginate_query(query, page, per_page=10):
    page = max(page or 1, 1)
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    return Pagination(items, page, per_page, total)
