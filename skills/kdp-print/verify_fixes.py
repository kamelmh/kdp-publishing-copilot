import fitz

doc = fitz.open(r"C:\Users\Admin\Projects\active\kdp-publishing-copilot\books\notary-log-book\interior_improved.pdf")
print("=== VERIFICATION AFTER FIXES ===")
print(f"Pages: {len(doc)}")
meta = doc.metadata
print(f"Title: {meta.get('title')}")
print(f"Author: {meta.get('author')}")

# Check bottom margin
print("\n--- Bottom Margin Check ---")
page = doc[2]  # Entry page 3
blocks = page.get_text("dict")["blocks"]
if blocks:
    min_y = min(b["bbox"][1] for b in blocks if "bbox" in b)
    bottom_margin = (648 - min_y) / 72
    print(f"Page 3: lowest content at {min_y:.1f}pt, bottom margin = {bottom_margin:.3f}\"")

# Check Notes pages have ruled lines
print("\n--- Notes Pages (117-120) ---")
for i in [116, 117, 118, 119]:
    page = doc[i]
    drawings = page.get_drawings()
    line_count = sum(1 for d in drawings if d["type"] == "l")
    print(f"Page {i+1}: {line_count} drawing operations (lines)")

# Check page 2
print("\n--- Page 2 (Instructions) ---")
page2 = doc[1]
text = page2.get_text()
print(f"Contains 'STATE-SPECIFIC': {'STATE-SPECIFIC' in text}")
print(f"Contains 'FEE SCHEDULE': {'FEE SCHEDULE' in text}")

# Check index columns
print("\n--- Index (page 113) ---")
page113 = doc[112]
text113 = page113.get_text()
print(f"Contains 'Doc Type': {'Doc Type' in text113}")

# Check no M logo on entry pages
print("\n--- Entry Page (page 3) ---")
page3 = doc[2]
text3 = page3.get_text()
print(f"Contains 'MERIDIAN PRESS': {'MERIDIAN PRESS' in text3}")
print(f"Contains 'NOTARIAL ACT RECORD': {'NOTARIAL ACT RECORD' in text3}")

doc.close()
