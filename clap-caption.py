import json


def parse_args():
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-cpu",
        "--no_cuda",
        action="store_true",
        help="use cpu (no use CUDA)"
    )
    parser.add_argument(
        "-p",
        "--print",
        action="store_true",
        help="print to console instead write jsonl"
    )
    parser.add_argument(
        "-m",
        "--model",
        default="clapcap",
        help="A model what you wanna use"
    )
    parser.add_argument(
        "wavs",
        nargs="+",
        help="path to audio file(s)"
    )
    parser.add_argument(
        "-b",
        "--beam_size",
        type=int,
        default=5,
        help="GPT-2 Beam Size"
    )
    parser.add_argument(
        "-t",
        "--temp",
        type=float,
        default=0.75,
        help="GPT-2 Temperature"
    )
    return parser.parse_args()


def load_tags(file_path='tags.json'):
    with open(file_path, 'r') as file:
        tags_data = json.load(file)
        tags = sum(tags_data.values(), [])
    return list(set(tags))


if __name__ == "__main__":
    cmds = parse_args()
    
    import os, glob, pathlib
    import torch
    from msclap import CLAP
    import librosa
    from tqdm import tqdm
    
    clap_model = CLAP(version = 'clapcap', use_cuda=not cmds.no_cuda)
    
    results = []
    
    for input_arg in tqdm(cmds.wavs, position=0):
        if os.path.isdir(input_arg):
            wavfiles = glob.glob(f"{input_arg}/**/*.*", recursive=True)
        else:
            wavfiles = [input_arg]
            
        for wavfile in tqdm(wavfiles, position=1):
            try:
                _, _ = librosa.load(wavfile, sr=None)
            except:
                print(f"{wavfile} is not audio file, skipped...")
                continue

            with torch.no_grad():
                captions = clap_model.generate_caption(audio_files=[wavfile], beam_size=cmds.beam_size, temperature=cmds.temp)
            
            results.append({
                wavfile: captions[0]
            })
            
            if cmds.print:
                print(f"{wavfile}: {captions[0]}")

            
        if not cmds.print:
            out_jsonl = f"{'_'.join(pathlib.Path(input_arg).as_posix().split("/")).replace(":", "")}.jsonl"
            with open(out_jsonl, 'w', encoding="utf-8") as f:
                f.writelines(json.dumps(l) + '\n' for l in results)