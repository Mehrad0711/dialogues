import argparse
import json
import os

from dialogues.risawoz.src.convert import build_dataset, build_db

parser = argparse.ArgumentParser()

parser.add_argument("--root", type=str, default='dialogues/risawoz/', help='code root directory')
parser.add_argument("--data_dir", type=str, default="data/original/", help="path to original data, relative to root dir")
parser.add_argument("--save_dir", type=str, default="data/", help="path to save preprocessed data, relative to root dir")
parser.add_argument("--setting", type=str, default="zh", help="en, zh, en_zh")
parser.add_argument("--splits", nargs='+', default=['valid'])

args = parser.parse_args()

mongodb_host = "mongodb://localhost:27017/"

risawoz_db = build_db(
    db_json_path=os.path.join(*[args.root, f'database/db_{args.setting}']),
    api_map=None,
    setting=args.setting,
    mongodb_host=mongodb_host,
)

original_data_path = os.path.join(*[args.root, args.data_dir])
processed_data_path = os.path.join(*[args.root, args.save_dir])

for split in args.splits:
    print(f"processing {split} data...")
    processed_data = build_dataset(os.path.join(original_data_path, f"{args.setting}_{split}.json"), risawoz_db, args.setting)

    # save converted files in JSON format
    with open(f"{processed_data_path}/{args.setting}_{split}.json") as f:
        gold_data = json.load(f)

    assert processed_data == gold_data
