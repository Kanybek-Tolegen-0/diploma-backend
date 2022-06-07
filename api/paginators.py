from rest_framework import pagination

class CustomLimitOffsetPaginator(pagination.LimitOffsetPagination):

    """
    Overriding
    :limit_query_param,
    :offset_query_param,
    :default_limit
    """
    
    default_limit = 10
    limit_query_param = 'paginate_by'
    offset_query_param = 'page'
