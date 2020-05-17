# wuchna/models.py
from cassandra.cqlengine import columns
from cassandra.cqlengine import models
from cassandra.cqlengine import usertype

#from pages.models import rpage_firstline_type, rpage_meta_type, rwuchna_html
# from cassandra.cqlengine.management import sync_table


class rpage_firstline_type(usertype.UserType):
    obj_type = columns.Text(required=False)
    categories = columns.List(columns.Text(required=False))
    apps = columns.Map(columns.Text(required=False), columns.Boolean(required=False))


class rpage_meta_type(usertype.UserType):
    meta_title = columns.Text(required=False)
    full_title = columns.Text(required=False)
    meta_dscr = columns.Text(required=False)
    meta_keywords = columns.Set(columns.Text(required=False))
    other_languages = columns.Map(columns.Text(required=False), columns.Text(required=False))
    other_html = columns.Text(required=False)


class rwuchna_html(usertype.UserType):
    wcontent = columns.Text(required=False)
    wcontext = columns.Map(columns.Text(required=False), columns.Integer())


class ResearchPagesModel(models.Model):
    __table_name__ = 'researchpages'
    url = columns.Text(required=True, primary_key=True)
    lang = columns.Text(primary_key=True, clustering_order="ASC")
    custom_footer = columns.Text(required=False)
    custom_header = columns.Text(required=False)
    firstline = columns.UserDefinedType(rpage_firstline_type)
    page_meta = columns.UserDefinedType(rpage_meta_type)
    page_references = columns.Text(required=False)
    section1 = columns.List(columns.UserDefinedType(rwuchna_html))
    section2 = columns.List(columns.UserDefinedType(rwuchna_html))
    section3 = columns.List(columns.UserDefinedType(rwuchna_html))
    section4 = columns.List(columns.UserDefinedType(rwuchna_html))
    section5 = columns.List(columns.UserDefinedType(rwuchna_html))
    section6 = columns.List(columns.UserDefinedType(rwuchna_html))
    section7 = columns.List(columns.UserDefinedType(rwuchna_html))
    section8 = columns.List(columns.UserDefinedType(rwuchna_html))
    section9 = columns.List(columns.UserDefinedType(rwuchna_html))
    images = columns.List(columns.UserDefinedType(rwuchna_html))
    videos = columns.List(columns.UserDefinedType(rwuchna_html))
    relations = columns.List(columns.UserDefinedType(rwuchna_html))

    class Meta:
        db_table = 'researchpages'
        verbose_name = 'research-pagesmodel'
        verbose_name_plural = 'research-pagesmodel'

    def __unicode__(self):
        return self.url