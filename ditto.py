import streamlit as st
import requests
import bs4
from bs4 import BeautifulSoup
import streamlit.components.v1 as components

st.header("DITTO — Duplicating Information To Transform Optimisations")

def get_soup(url):
	res = requests.get(url)
	soup = BeautifulSoup(res.content, 'html.parser')
	return soup

def remove_tags(soup):
    for data in soup(['style', 'script']):
        data.decompose()
    ps = soup.find_all(['h1', 'h2', 'h3', 'p', 'li', 'table'])
    for p in ps:
    	try:
    		p.span.unwrap()
    	except:
    		continue
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

webpage = st.text_input("Enter a webpage to extract")
html_file = st.file_uploader("Upload your HTML file", type="html", accept_multiple_files=False)
submit = st.button("Submit")

if html_file and submit:
	with html_file as h:
		content = h.read()
		soup = BeautifulSoup(content, 'html.parser')
		v_soup = remove_tags(soup)
		vg_soup = remove_attrs(v_soup)
		st.html(str(vg_soup))
elif webpage and submit:
	soup = get_soup(webpage)
	v_soup = remove_tags(soup)
	vg_soup = remove_attrs(v_soup)
	st.html(str(vg_soup))
