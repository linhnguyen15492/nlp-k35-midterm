"""
Entrypoint for Sentence Alignment pipeline.

Usage:
    python src/sentence_alignment/run.py
    python src/sentence_alignment/run.py --work-id an-nam-chi-luoc
    python src/sentence_alignment/run.py --method labse
    python src/sentence_alignment/run.py --method auto_translate
    python src/sentence_alignment/run.py --method greedy
"""

# TODO: parse CLI args (--work-id, --method)
# TODO: load config via config_loader.load_config()
# TODO: for each work (filtered by --work-id if given):
#   TODO: load processed/<id>/han.json and viet.json
#   TODO: aligner.align(han_sentences, viet_sentences, method) → pairs
#   TODO: (optional) char_aligner.verify(pairs) → annotated pairs
#   TODO: corpus_builder.build(pairs, work_id, work_index) → TSV rows
#   TODO: write corpus/<id>/HVB_corpus.tsv
# TODO: after all works: merge all TSVs → corpus/HVB_corpus_all.tsv
