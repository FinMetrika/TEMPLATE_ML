# DATACLASS
#MODEL_NAME_HR="meta-llama/Llama-2-7b-hf"
PROBA="ema"
python3 src/main.py \
    proba $PROBA \

# ARGPARSE
# export FILE_NAMES='["keksDejan1.csv", "keksIta.csv"]'
# python3 src/main.py \
#     --file_names "$FILE_NAMES"