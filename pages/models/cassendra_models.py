# wuchna/models.py
# from follow import utils

from cassandra.cqlengine import columns
from cassandra.cqlengine import models
from cassandra.cqlengine import usertype


class page_firstline_type(usertype.UserType):
    obj_type = columns.Text(required=False)
    categories = columns.List(columns.Text(required=False))
    apps = columns.Map(columns.Text(required=False), columns.Boolean(required=False))


class page_meta_type(usertype.UserType):
    meta_title = columns.Text(required=False)
    full_title = columns.Text(required=False)
    meta_dscr = columns.Text(required=False)
    meta_keywords = columns.Set(columns.Text(required=False))
    other_languages = columns.Map(columns.Text(required=False), columns.Text(required=False))
    other_html = columns.Text(required=False)


class wuchna_html(usertype.UserType):
    wcontent = columns.Text(required=False)
    wcontext = columns.Map(columns.Text(required=False), columns.Integer())


class PagesModel(models.Model):
    __table_name__ = 'pages'
    url = columns.Text(required=True, primary_key=True)
    lang = columns.Text(primary_key=True, clustering_order="ASC")
    custom_footer = columns.Text(required=False)
    custom_header = columns.Text(required=False)
    firstline = columns.UserDefinedType(page_firstline_type)
    page_meta = columns.UserDefinedType(page_meta_type)
    page_references = columns.Text(required=False)
    section1 = columns.List(columns.UserDefinedType(wuchna_html))
    section2 = columns.List(columns.UserDefinedType(wuchna_html))
    section3 = columns.List(columns.UserDefinedType(wuchna_html))
    section4 = columns.List(columns.UserDefinedType(wuchna_html))
    section5 = columns.List(columns.UserDefinedType(wuchna_html))
    section6 = columns.List(columns.UserDefinedType(wuchna_html))
    section7 = columns.List(columns.UserDefinedType(wuchna_html))
    section8 = columns.List(columns.UserDefinedType(wuchna_html))
    section9 = columns.List(columns.UserDefinedType(wuchna_html))
    images = columns.List(columns.UserDefinedType(wuchna_html))
    videos = columns.List(columns.UserDefinedType(wuchna_html))
    relations = columns.List(columns.UserDefinedType(wuchna_html))

    class Meta:
        db_table = 'pages'
        verbose_name = 'pagesmodel'
        verbose_name_plural = 'pagesmodel'

    def __unicode__(self):
        return self.url

# utils.register(PagesModel)
