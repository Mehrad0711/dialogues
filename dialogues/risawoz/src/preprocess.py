import argparse
import json
import os

from dialogues.risawoz.main import Risawoz
from dialogues.utils import get_commit


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=str, default='dialogues/risawoz/', help='code root directory')
    parser.add_argument("--data_dir", type=str, default="data", help="path to save original data, relative to root dir")
    parser.add_argument(
        "--save_dir", type=str, default="data/preprocessed", help="path to save preprocessed data, relative to root dir"
    )
    parser.add_argument(
        "--detail", type=bool, default=False, help="whether to return dict annotations, used for data augmentation"
    )
    parser.add_argument("--setting", type=str, default="en", help="en, zh, en_zh")

    parser.add_argument("--max_history", type=int, default=2)
    parser.add_argument("--splits", nargs='+', default=['train', 'eval', 'test'])
    parser.add_argument("--version", type=str, default='11')
    parser.add_argument("--fewshot_percent", type=int, default=0)
    parser.add_argument("--sampling", choices=["sequential", "balanced"], default="sequential")
    parser.add_argument("--use_user_acts", action='store_true')
    parser.add_argument("--gen_lev_span", action='store_true')
    parser.add_argument("--gen_full_state", action='store_true')
    parser.add_argument("--last_two_agent_turns", action='store_true')
    parser.add_argument("--english_slots", action='store_true')
    parser.add_argument("--use_natural_response", action='store_true')
    parser.add_argument("--only_user_rg", action='store_true')

    parser.add_argument("--max_input_output_length", default='1000')

    args = parser.parse_args()

    dataset = Risawoz()

    path_train = [f"data/{args.setting}_train.json"]
    path_fewshot = [f"data/{args.setting}_fewshot.json"]
    path_dev = [f"data/{args.setting}_valid.json"]
    path_test = [f"data/{args.setting}_test.json"]

    # path_train = ["data/zh_train.json", "data/en_train.json"]
    # path_fewshot = ["data/zh_fewshot.json", "data/en_fewshot.json"]
    # path_dev = ["data/zh_valid.json", "data/en_valid.json"]
    # path_test = ["data/zh_test.json", "data/en_test.json"]

    path_train = [os.path.join(args.root, p) for p in path_train]
    path_fewshot = [os.path.join(args.root, p) for p in path_fewshot]
    path_dev = [os.path.join(args.root, p) for p in path_dev]
    path_test = [os.path.join(args.root, p) for p in path_test]

    data_train, data_fewshot, data_dev, data_test = dataset.prepare_data(args, path_train, path_fewshot, path_dev, path_test)

    args.commit = get_commit()

    save_dir = os.path.join(*[args.root, args.save_dir, f'{args.setting}_v{args.version}'])
    os.makedirs(save_dir, exist_ok=True)

    for (split, data) in zip(['train', 'fewshot', 'valid', 'test'], [data_train, data_fewshot, data_dev, data_test]):
        with open(os.path.join(save_dir, f"{split}.json"), "w") as f:
            if data:
                json.dump({"args": vars(args), "data": data}, f, indent=True, ensure_ascii=False)
                print(split, len(data))

    # with open(os.path.join(f"./data_samples/v{args.version}.json"), "w") as f:
    #     json.dump({"data": data_test[:30]}, f, indent=True, ensure_ascii=False)


if __name__ == "__main__":
    main()
