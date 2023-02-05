from parse_html import ParseHtml
from metadata_structure import MetadataStruture

coleta = False
if coleta:
    parser_html = ParseHtml()
    parser_html.process()
    structure = MetadataStruture()
    for data_frame, subtitle, title, data_name in parser_html.list_df():
        structure.save_parquet(subtitle=subtitle,
                               title=title,
                               data_frame=data_frame,
                               stage='raw',
                               data_name=data_name)
