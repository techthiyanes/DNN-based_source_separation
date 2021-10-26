# MUSDB18を使用した楽音分離
## 実験結果
SDR [dB] (`museval`によって計算された各曲のSDRの中央値の中央値)
| Model | Bass | Drums | Other | Vocals | Accompaniment | Average |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| MMDense | - | - | - | - | - | - |
| MMDenseLSTM | - | - | - | - | - | - |
| Conv-TasNet | 5.95 | 6.11 | 3.78 | 5.59 | 11.90 | 5.36 |
| CUNet | - | - | - | - | - | - |
| Meta-TasNet | - | - | - | - | - | - |
| UMX | 5.02 | 6.06 | 4.00 | 6.14 | 12.18 | 5.30 |
| X-UMX | - | - | - | - | - | - |
| D3Net | 5.24 | 6.71 | 4.59 | 6.97 | 13.22 | 5.88 |
| LaSAFT | - | - | - | - | - | - |
| MRX | - | - | - | - | - | - |

## 分離の例
- Conv-TasNet: `egs/tutorials/conv-tasnet/separate_music_ja.ipynb`を見るか， [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tky823/DNN-based_source_separation/blob/main/egs/tutorials/conv-tasnet/separate_music_ja.ipynb)にとんでください．
- UMX: `egs/tutorials/umx/separate_music_ja.ipynb`を見るか， [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tky823/DNN-based_source_separation/blob/main/egs/tutorials/umx/separate_music_ja.ipynb)にとんでください．
- D3Net: `egs/tutorials/d3net/separate_music_ja.ipynb`を見るか， [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tky823/DNN-based_source_separation/blob/main/egs/tutorials/d3net/separate_music_ja.ipynb)にとんでください．