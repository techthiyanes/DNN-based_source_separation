#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

import torch
import torch.nn as nn

from utils.utils import set_seed
from dataset import TrainDataLoader
from adhoc_dataset import SpectrogramTrainDataset, SpectrogramEvalDataset, EvalDataLoader
from adhoc_driver import AdhocTrainer
from models.d3net import D3Net
from criterion.distance import MeanSquaredError

parser = argparse.ArgumentParser(description="Training of D3Net")

parser.add_argument('--musdb18_root', type=str, default=None, help='Path to MUSDB18')
parser.add_argument('--is_wav', type=int, default=0, help='0: extension is wav (MUSDB), 1: extension is not .wav, is expected .mp4 (MUSDB-HQ)')
parser.add_argument('--config_path', type=str, default=None, help='Path to model configuration file')
parser.add_argument('--sr', type=int, default=10, help='Sampling rate')
parser.add_argument('--patch_size', type=int, default=256, help='Patch size')
parser.add_argument('--valid_duration', type=float, default=30, help='Max duration for validation')
parser.add_argument('--fft_size', type=int, default=4096, help='FFT length')
parser.add_argument('--hop_size', type=int, default=1024, help='Hop length')
parser.add_argument('--window_fn', type=str, default='hamming', help='Window function')
parser.add_argument('--sources', type=str, default="[drums,bass,other,vocals]", help='Source names')
parser.add_argument('--target', type=str, default=None, choices=['drums', 'bass', 'other', 'vocals'], help='Target source name')
parser.add_argument('--criterion', type=str, default='mse', choices=['mse'], help='Criterion')
parser.add_argument('--optimizer', type=str, default='adam', choices=['sgd', 'adam', 'rmsprop'], help='Optimizer, [sgd, adam, rmsprop]')
parser.add_argument('--lr', type=float, default=0.001, help='Learning rate. Default: 0.001')
parser.add_argument('--anneal_lr', type=float, default=0.0001, help='Learning rate. Default: 0.0001')
parser.add_argument('--weight_decay', type=float, default=0, help='Weight decay (L2 penalty). Default: 0')
parser.add_argument('--max_norm', type=float, default=None, help='Gradient clipping')
parser.add_argument('--batch_size', type=int, default=4, help='Batch size. Default: 128')
parser.add_argument('--epochs', type=int, default=50, help='Number of epochs')
parser.add_argument('--anneal_epoch', type=int, default=40, help='Epoch when annealing')
parser.add_argument('--model_dir', type=str, default='./tmp/model', help='Model directory')
parser.add_argument('--loss_dir', type=str, default='./tmp/loss', help='Loss directory')
parser.add_argument('--sample_dir', type=str, default='./tmp/sample', help='Sample directory')
parser.add_argument('--continue_from', type=str, default=None, help='Resume training')
parser.add_argument('--use_cuda', type=int, default=1, help='0: Not use cuda, 1: Use cuda')
parser.add_argument('--overwrite', type=int, default=0, help='0: NOT overwrite, 1: FORCE overwrite')
parser.add_argument('--seed', type=int, default=42, help='Random seed')

def main(args):
    set_seed(args.seed)
    
    args.sources = args.sources.replace('[', '').replace(']', '').split(',')
    patch_samples = (args.hop_size * (args.patch_size - 1 - (args.fft_size - args.hop_size) // args.hop_size - 1) + args.fft_size)
    max_samples = int(args.valid_duration * args.sr)
    samples_per_epoch = None
    
    train_dataset = SpectrogramTrainDataset(args.musdb18_root, fft_size=args.fft_size, hop_size=args.hop_size, sr=args.sr, patch_samples=patch_samples, samples_per_epoch=samples_per_epoch, sources=args.sources, target=args.target, augmentation=True, is_wav=args.is_wav)
    valid_dataset = SpectrogramEvalDataset(args.musdb18_root, fft_size=args.fft_size, hop_size=args.hop_size, sr=args.sr, patch_samples=patch_samples, max_samples=max_samples, sources=args.sources, target=args.target, is_wav=args.is_wav)
    
    print("Training dataset includes {} samples.".format(len(train_dataset)))
    print("Valid dataset includes {} samples.".format(len(valid_dataset)))
    
    loader = {}
    loader['train'] = TrainDataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    loader['valid'] = EvalDataLoader(valid_dataset, batch_size=1, shuffle=False)
    
    if args.max_norm is not None and args.max_norm == 0:
        args.max_norm = None
    model = D3Net.build_from_config(config_path=args.config_path)

    print(model)
    print("# Parameters: {}".format(model.num_parameters), flush=True)
    
    if args.use_cuda:
        if torch.cuda.is_available():
            model.cuda()
            model = nn.DataParallel(model)
            print("Use CUDA")
        else:
            raise ValueError("Cannot use CUDA.")
    else:
        print("Does NOT use CUDA")
        
    # Optimizer
    if args.optimizer == 'sgd':
        optimizer = torch.optim.SGD(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    elif args.optimizer == 'adam':
        optimizer = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    elif args.optimizer == 'rmsprop':
        optimizer = torch.optim.RMSprop(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    else:
        raise ValueError("Not support optimizer {}".format(args.optimizer))
    
    # Criterion
    if args.criterion == 'mse':
        criterion = MeanSquaredError(dim=(1,2,3))
    else:
        raise ValueError("Not support criterion {}".format(args.criterion))
    
    trainer = AdhocTrainer(model, loader, criterion, optimizer, args)
    trainer.run()

if __name__ == '__main__':
    args = parser.parse_args()
    print(args)
    main(args)
