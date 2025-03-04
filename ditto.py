import streamlit as st
import requests
import bs4
from bs4 import BeautifulSoup
import streamlit.components.v1 as components

TITLE = "DITTO — Duplicating Information To Transform Optimisations"

st.set_page_config(page_title=TITLE)
st.header(TITLE)

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

st.sidebar.subheader("Helpful info")

with st.sidebar.expander("How to use DITTO 👛", expanded=False):

	st.markdown(
		"""
		Enter the URL of the page you want to copy and paste unstyled text from or upload a HTML file.

		"""
    )

with st.sidebar.expander("Things to 🐻 in mind", expanded=False):

	st.markdown(
		"""
		- As not all webpages are set up the same, you might find it challenging to copy and paste text from a page—or not at all.
		- Text may not be completely unstyled but I will endeavour to include different elements to strip out. If you spot anything that keeps coming up, please let me know.

		"""
    )

with st.sidebar.expander("Credits 🏆", expanded=False):

	st.markdown(
		"""
		DITTO was created by [Luke Davis](https://lukealexdavis.co.uk/). If you have any feedback or find any bugs, please let me know.
	    """
	)

def get_soup(url):
	try:
		res = requests.get(url, headers=headers)
		soup = BeautifulSoup(res.content, 'html.parser')
		return soup
	except Exception as e:
		st.error(e)

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
html_file = st.file_uploader("Or upload your HTML file", type="html", accept_multiple_files=False)
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
