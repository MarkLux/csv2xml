# -*- coding:utf-8
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import json
import csv
import settings
import sys
from sys import argv
reload(sys)
sys.setdefaultencoding('utf8')

def csv2dict(file_path):
    # convert the input csv into a dict.
    raw_data = [];
    result= [];
    with open(file_path) as f:
        reader = csv.reader(f)
        for row in reader:
            raw_data.append(row)
    # the first row contains the key, pop it
    columns = [trim_chn(k) for k in raw_data.pop(0)]
    for datum in raw_data:
        row_dict = {}
        for i in range(0, len(datum)):
            row_dict[columns[i]] = datum[i]
        result.append(row_dict)
        # pop useless key
        row_dict.pop('')
    return result

def trim_chn(text):
    # try to trim all chinese characters in the text, only reserve english
    first_level =  ''.join([i if ord(i) < 128 else '' for i in text])
    return first_level.replace('(', '').replace(')', '')

# main work function
def dict2xml(data_dict, doc_root):
    row_ele = ET.SubElement(doc_root, settings.single_row_tag)
    # general tag
    general_ele = ET.SubElement(row_ele, 'General')
    # spatio_temporal tag
    st_ele = ET.SubElement(row_ele, 'SpatioTemporal')
    attr_ele_dict = {}    
    for (k, v) in data_dict.items():
        if k in settings.spatio_temporal_cols:
            ele = ET.SubElement(st_ele, k)
            handle_ele(ele, k, trans_val_type(k, v))
        elif k in settings.attributes:
            target_tag_name = settings.attributes[k]
            if target_tag_name in attr_ele_dict.keys():
                attr_ele_dict[target_tag_name][k] = v
            else:
                attr_ele_dict[target_tag_name] = {k: v}
        else:
            ele = ET.SubElement(general_ele, k)
            handle_ele(ele, k, trans_val_type(k, v))
    # need a walk of tree to add the attributes.
    handle_attr(row_ele, attr_ele_dict)
    print 'successful transfered a row!'

# recursive handle columns.
def handle_ele(parent_element, sub_key, sub_val):
    if is_type_of(sub_val, 'dict'):
        for (k, v) in sub_val.items():
            sub_ele = ET.SubElement(parent_element, k)
            handle_ele(sub_ele, k, v)
    elif is_type_of(sub_val, 'list'):
        # igonre the end 's' and create new tags
        for v in sub_val:
            tag_name = sub_key[:-1] if sub_key.endswith('s') else 'value'
            sub_ele = ET.SubElement(parent_element, tag_name)
            handle_ele(sub_ele, 'value', v)
    else:
        # seen as text
        parent_element.text = sub_val

# recursive handle atrributes
def handle_attr(root_element, attr_dict):
    attrs = attr_dict.get(root_element.tag)
    if attrs:
        for (k, v) in attrs.items():
            root_element.set(k, v)
    for child_element in root_element.getchildren():
        handle_attr(child_element, attr_dict)

def trans_val_type(k, v):
    if k in settings.special_column_types:
        type2convert = settings.special_column_types[k]
        if type2convert == 'json':
            return json.loads(v)
        # etc...
    else:
        return v

def is_type_of(var, type_name):
    return (type(var).__name__ == type_name)

def output_xml(element, output_file):
    raw_str = ET.tostring(element, 'utf-8')
    with open(output_file, 'w+') as f:
        f.write(raw_str)
    return

if __name__ == "__main__":
    if len(argv) != 2:
        print 'wrong argument nums!'
        exit(0)
    file_name = argv[1]
    data = csv2dict(file_name)
    doc_root = ET.Element(settings.top_element_tag)
    i = 0
    total = len(data)
    for row in data:
        try:
            dict2xml(row, doc_root)
            i += 1
            print 'sucessfully transfered ' + str(i) + '/' + str(total) + ' rows'
        except Exception as e:
            print 'Fail to transfer row: ' + e
    print 'trasfermation ended, output file is --> result.xml'
    output_xml(doc_root, 'result.xml')