import fitz

doc = fitz.open(r"C:\Users\Admin\Projects\active\kdp-publishing-copilot\books\notary-log-book\interior_improved.pdf")

# Check page 117 content
page = doc[116]
text = page.get_text()
print("Page 117 text:")
print(repr(text[:500]))

# Check drawings
drawings = page.get_drawings()
print(f"\nDrawings: {len(drawings)}")
for d in drawings[:5]:
    print(f"  Type: {d['type']}, Rect: {d.get('rect', 'N/A')}")

# Check page 3 for comparison
page3 = doc[2]
drawings3 = page3.get_drawings()
print(f"\nPage 3 drawings: {len(drawings3)}")

doc.close()
