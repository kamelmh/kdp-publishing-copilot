import fitz
import os

pdf_path = r"C:\Users\Admin\Projects\active\kdp-publishing-copilot\books\notary-log-book\interior_improved.pdf"
out_dir = r"C:\Users\Admin\Projects\active\kdp-publishing-copilot\claude-gui-package\visual-inspection"

doc = fitz.open(pdf_path)

pages = [0, 1, 2, 112, 113, 116]  # 0-indexed: pages 1,2,3,113,114,117

for p in pages:
    page = doc[p]
    pix = page.get_pixmap(matrix=fitz.Matrix(150/72, 150/72))  # 150 DPI
    out_file = os.path.join(out_dir, f"page-{p+1:03d}.png")
    pix.save(out_file)
    print(f"Rendered page {p+1}: {out_file}")

doc.close()
print("Done.")
