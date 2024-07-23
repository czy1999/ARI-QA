# 🎉ARI-QA

[![language-python3](https://img.shields.io/badge/Language-Python3-blue.svg?style=flat-square)](https://www.python.org/)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg?style=flat-square)](https://github.com/czy1999/MultiTQ/issues)

This is the code for the paper [Temporal Knowledge Question Answering via Abstract Reasoning Induction](https://arxiv.org/pdf/2311.09149) (Chen et al., ACL 2024).

## Architecture of ARI-QA
![Architecture of ARI-QA](https://s21.ax1x.com/2024/07/23/pkHCT58.png)

**ARI (Abstract Reasoning Induction)** is an innovative framework designed to enhance the temporal reasoning capabilities of Large Language Models (LLMs). By dividing the reasoning process into two distinct phases—Knowledge-agnostic and Knowledge-based—ARI aims to mitigate the issues of hallucinations and improve LLMs' ability to integrate abstract methodologies derived from historical data. 

## Datasets

🤗MultiTQ Datasets Link: https://huggingface.co/datasets/chenziyang/MultiTQ

🤗CronQuestion Datasets Link: https://github.com/apoorvumang/CronKGQA

|Example questions|	Answer|
|  ----  | ----  |
|Who condemned Abhisit Vejjajiva in May 2010?	|Thailand
|Who was the first to visit the Middle East in 2008?	|Frank Bainimarama|
|When did the Aam Aadmi Party first negotiated with Harish Rawat?|	2015-12-13|
|Who expressed intent to engage in diplomatic cooperation with Ethiopia before Jun 25th, 2006?	|China|



Dataset used in this paper can be found in ./data folder. 

```bash
git clone git@github.com:czy1999/ARI-QA.git

cd ./ARI-QA/data
unzip data.zip
```



## Running the code
 running jupyter notebook
```bash
# For CronQuestions
# run ./CronQuestions/run_cronquestions.ipynb

# For MultiTQ
# run ./MultiTQ/run_multitq.ipynb
 ```
 Note: Before running the code, make sure to input your OpenAI key in utils.py.

## Cite

If you find our method, code, or experimental setups useful, please cite our paper:


```bibtex
@article{chen2023temporal,
  title={Temporal Knowledge Question Answering via Abstract Reasoning Induction},
  author={Chen, Ziyang and Li, Dongfang and Zhao, Xiang and Hu, Baotian and Zhang, Min},
  journal={arXiv preprint arXiv:2311.09149},
  year={2023}
}
```

