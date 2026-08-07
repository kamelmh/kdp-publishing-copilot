import fitz

# Check interior
doc = fitz.open(r"C:\Users\Admin\Projects\active\kdp-publishing-copilot\books\notary-log-book\interior.pdf")
meta = doc.metadata
print("=== INTERIOR ===")
print(f"Pages: {len(doc)}")
print(f"Title: {meta.get('title')}")
print(f"Author: {meta.get('author')}")

# Check page 117 for ruled lines
page117 = doc[116]
drawings = page117.get_drawings()
print(f"Page 117 drawings: {len(drawings)}")
doc.close()

# Check cover
doc2 = fitz.open(r"C:\Users\Admin\Projects\active\kdp-publishing-copilot\books\notary-log-book\cover-wrap-green.pdf")
print("\n=== COVER ===")
print(f"Pages: {len(doc2)}")
page = doc2[0]
text = page.get_text()
print(f"Contains MERIDIAN PRESS: {'MERIDIAN PRESS' in text}")
doc2.close()
