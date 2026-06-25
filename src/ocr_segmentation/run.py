"""
Entrypoint for OCR + Segmentation pipeline.

Usage:
    python src/ocr_segmentation/run.py
    python src/ocr_segmentation/run.py --work-id an-nam-chi-luoc
    python src/ocr_segmentation/run.py --work-id an-nam-chi-luoc --lang han
"""

# TODO: parse CLI args (--work-id, --lang)
# TODO: load config via config_loader.load_config()
# TODO: for each work (filtered by --work-id if given):
#   TODO: for each resource (filtered by --lang if given):
#     TODO: if format == "pdf"        → pdf_to_images.convert() → temp image list
#     TODO: if format == "images"     → read images from directory
#     TODO: if format == "text"       → skip OCR, read raw text
#     TODO: if format == "mixed_page" → pdf_to_images.convert() → temp images
#     TODO: ocr_engine.run(images, lang, format) → raw text lines
#     TODO: if lang == "han"          → bbox_sort.sort(lines)
#     TODO: write ocr_output/<id>/<lang>.txt
#     TODO: segmenter.segment(lines, lang) → sentences
#     TODO: write processed/<id>/<lang>.json
