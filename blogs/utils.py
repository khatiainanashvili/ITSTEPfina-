from django.core.paginator import Page, Paginator, PageNotAnInteger, EmptyPage

class CustomPaginator(Paginator):

    def get_page_range(self, current_page, range_size=2):
    
        start = max(current_page - range_size, 1)
        end = min(current_page + range_size, self.num_pages) + 1
        return range(start, end)
