import matplotlib.pyplot as plt
import IPython.display as ipd

import os
import json
import math
import torch


import commons
import utils
from models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence

from scipy.io.wavfile import write


def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm
hps = utils.get_hparams_from_file("pretrained_model/config.json")
net_g1 = SynthesizerTrn(
    len(hps.symbols),
    hps.data.filter_length // 2 + 1,
    hps.train.segment_size // hps.data.hop_length,
    n_speakers=hps.data.n_speakers,
    **hps.model).cuda()
model1 = net_g1.eval()
model1 = utils.load_checkpoint("pretrained_model/alice.pth", net_g1, None)

net_g2 = SynthesizerTrn(
    len(hps.symbols),
    hps.data.filter_length // 2 + 1,
    hps.train.segment_size // hps.data.hop_length,
    n_speakers=hps.data.n_speakers,
    **hps.model).cuda()
model2 = net_g2.eval()

model2 = utils.load_checkpoint("pretrained_model/yuuka.pth", net_g2, None)
