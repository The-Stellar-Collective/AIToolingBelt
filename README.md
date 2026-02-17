# AIToolingBelt

En samling verktyg och guider för AI-integration.

## Dokumentation

- **[Installation av AI-verktyg (CLI & Desktop Apps)](./CLI_INSTALLATIONSGUIDE.md)** - Komplett guide för installation av Claude, ChatGPT och Gemini på Mac, Windows och Linux
- **[Historia över AI-verktyg](./HISTORY.md)** - Utvecklingshistoria, design-filosofier och tankar bakom varje verktyg
- **[Utvecklarverktyg](./TOOLS.md)** - Installation av VS Code och rekommenderade Markdown-extensions på alla plattformar
- **[Filosofi bakom AI och Matematik](./FILOSOFI.md)** - Filosofiska motsättningar, från Quetelet och Markov till modern AI

---

## Idéhistorisk tolkning: Quetelet, Nekrasov, Markov

Den här historien kan också läsas genom en äldre statistisk lins:

- **Quetelet (1796-1874):** motsvarar hur sökmotorer fungerade i praktiken, där många källor vägs ihop för att hitta en gemensam sanning.  
  ![Adolphe Quetelet](https://commons.wikimedia.org/wiki/Special:FilePath/Adolphe%20Qu%C3%A9telet%20by%20Joseph-Arnold%20Demannez.jpg)
- **Nekrasov (1853-1924):** motsvarar vad man länge trodde att AI skulle ge, en mer entydig och samlad sanning med tydliga regler.  
  ![Pavel Nekrasov](https://commons.wikimedia.org/wiki/Special:FilePath/NekrasovPA-2.jpg)
- **Markov (1856-1922):** motsvarar vad vi faktiskt fick, system där betydelse skapas sekventiellt av kontext och beroenden mellan steg.  
  ![Andrey Markov](https://commons.wikimedia.org/wiki/Special:FilePath/AAMarkov.jpg)

Kort sagt: från sökningens "genomsnittliga sanning", via förväntan om en enhetlig AI-sanning, till dagens kontextuella och kedjebaserade språkmodeller.

## Tidslinje
 1. GPU-Computing Infrastructure (2004-2008)
  - NVIDIA CUDA möjliggör parallell programmering
  - 100x snabbare än CPUs för ML

 2. Deep Learning Frameworks (2011-2015)
  - Theano, Caffe, TensorFlow, PyTorch
  - Automatisk differentiering och GPU-acceleration

 3. Large Datasets (2010-2016)
  - ImageNet, Common Crawl, COCO
  - Du kan inte träna utan data

 4. RNNs & LSTMs (2010-2014)
  - Tidigare sekvensiella modeller
  - Recurrent Neural Networks
  - Long Short-Term Memory

 5. Attention Mechanisms (2014-2015)
  - Löste bottlenecks i RNNs
  - Modeller kunde fokusera på relevant info

 6. Word Embeddings (2013-2015)
  - Word2Vec, GloVe, FastText
  - Ord som numeriska vektorer

 7. Normalization & Regularization (2014-2015)
  - Batch Norm, Layer Norm
  - Möjliggjorde djupa nätverk

 8. Optimization Algorithms (2011-2014)
  - Adam optimizer blir standard
  - Snabbare training

 9. Transfer Learning (2012-2015)
  - Pre-train på stor dataset, fine-tune på ny uppgift
  - Demokratiserade AI

10. Positional Encoding (2016)
  - Hur modeller vet ordningen på tokens

11. Massive Computational Resources (2014-2016)
  - Cloud computing möjliggör experimentering
  - TPUs lanseras

12. Attention is All You Need Insight (2016)
  - Insikten att man inte behövde RNNs
  - Vägen till ren attention-baserad arkitektur

#### Citat från Travis om inspirationen
*"Jag ville visa att du inte behöver vänta på stora företag för att bygga användbara verktyg.
En utvecklare, några timmar kod, och plötsligt har du något som tusentals människor vill använda."*

** 2022 Skaparen av chatgpt cli **
*"Developers är problem-lösare. Vi bygger saker för att lösa våra egna problem,
och ofta blir dessa saker till något större än vi förväntat oss."* Travis Fischer

2023 Gemini/Google och Anthropic/Claude hängde på

**2024 Dario Amodei om MCP-visionen:**

*"Vi tror att framtiden för AI inte är isolerade modeller, utan modeller som är intimt
integrerade med människors verktyg och system. MCP är vår försök att göra detta på ett
öppet och standardiserat sätt."*

*"Precis som HTTP blev standarden för webben, vill vi att MCP ska bli standarden för
hur AI-modeller integreras med världen omkring dem."*

# Kombination

* Administration
* ordna information
* Insikter
* Delegera