import fitz

doc = fitz.open(r"C:\Users\Admin\Projects\active\kdp-publishing-copilot\books\notary-log-book\interior_improved.pdf")
print("=== VERIFICATION ===")
print(f"Pages: {len(doc)}")
meta = doc.metadata
print(f"Title: {meta.get('title', 'EMPTY')}")
print(f"Author: {meta.get('author', 'EMPTY')}")
print(f"Creator: {meta.get('creator', 'EMPTY')}")

# Check page numbers
print("\n--- Page Numbers ---")
for i in [2, 50, 112, 113, 116, 117, 119]:
    if i < len(doc):
        page = doc[i]
        text = page.get_text()
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        print(f"Page {i+1}: last lines = {lines[-3:]}")

# Check index has Document Type column
print("\n--- Index Columns (page 113) ---")
page113 = doc[112]
text113 = page113.get_text()
print(text113[:500])

# Check notes have ruled lines (page 117)
print("\n--- Notes Page (page 117) ---")
page117 = doc[116]
text117 = page117.get_text()
print(text117[:300])

doc.close()
