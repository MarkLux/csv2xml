# -*- coding:utf-8

# define the level relations between keys(if you need)
parents = {}

# define which columns will be process as attributes, v -> tag_col, k -> attribute_col
attributes = {
    'hid': 'hotel'
}

# define the time / space columns, other will be set into general
spatio_temporal_cols = ['time', 'latitude', 'longitude']

# define special column types, other will be processed as plain text.
special_column_types = {
    'room_beds': 'json',
    'photos': 'json'
}

# define the top element tag name
top_element_tag = 'hotels'

# define the single row tag name
single_row_tag = 'hotel'