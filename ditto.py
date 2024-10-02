import streamlit as st
import bs4
from bs4 import BeautifulSoup
import streamlit.components.v1 as components

st.header("DITTO — Duplicating Information To Transform Optimisations")

def remove_tags(soup):
    for data in soup(['style', 'script']):
        data.decompose()
    ps = soup.find_all(['h1', 'h2', 'h3', 'p', 'li'])
    for p in ps:
    	p.span.unwrap()
    return soup

def remove_attrs(soup):
	REMOVE_ATTRIBUTES = [
	    'lang','language','onmouseover','onmouseout','script','style','font',
	    'dir','face','size','color','style','class','width','height','hspace',
	    'border','valign','align','background','bgcolor','link','vlink',
	    'alink','cellpadding','cellspacing', 'id', 'rowspan', 'colspan']
	for tag in soup.descendants:
	    if isinstance(tag, bs4.element.Tag):
	        tag.attrs = {key: value for key, value in tag.attrs.items()
	                     if key not in REMOVE_ATTRIBUTES}
	return soup

html_file = st.file_uploader("Upload your HTML file", type="html", accept_multiple_files=False)

if html_file:
	with html_file as h:
		content = h.read()
		soup = BeautifulSoup(content, 'html.parser')
		v_soup = remove_tags(soup)
		vg_soup = remove_attrs(v_soup)
		st.html(str(vg_soup))