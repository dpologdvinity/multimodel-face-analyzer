# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/dpologdvinity/multimodel-face-analyzer/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                          |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|---------------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| src/face\_analyzer/app.py                     |       79 |       79 |       30 |        0 |      0% |     3-200 |
| src/face\_analyzer/attributes/\_lock.py       |       15 |        1 |        4 |        1 |     89% |        16 |
| src/face\_analyzer/attributes/accessories.py  |       87 |       44 |       38 |        3 |     46% |17-19, 24-29, 34-40, 67-\>53, 78-84, 94-120 |
| src/face\_analyzer/attributes/age.py          |       46 |        5 |        8 |        0 |     91% |16-18, 77-78 |
| src/face\_analyzer/attributes/emotion.py      |      105 |       33 |       22 |        3 |     70% |35-42, 47-54, 59-66, 71-79, 88, 89-\>91, 137, 159-160, 164-165 |
| src/face\_analyzer/attributes/race.py         |       38 |        4 |        2 |        0 |     90% |     92-97 |
| src/face\_analyzer/attributes/transformers.py |      212 |       99 |       58 |        5 |     50% |31-47, 57-59, 72-94, 101-107, 112-116, 121-125, 130-138, 148, 155-176, 181-192, 199-216, 225-232, 310, 319, 348, 367 |
| src/face\_analyzer/core/image\_utils.py       |       84 |       43 |       26 |       10 |     48% |16-21, 57, 67-71, 77-86, 91-92, 99-109, 114-115, 121-127, 132-133, 149, 151, 153, 155, 157, 159, 163, 165, 167, 169 |
| src/face\_analyzer/demo.py                    |       49 |        1 |        8 |        1 |     96% |       129 |
| src/face\_analyzer/detectors/factory.py       |       47 |        3 |       24 |        3 |     92% |31, 33, 35 |
| src/face\_analyzer/detectors/retinaface.py    |       67 |       50 |       12 |        1 |     23% |26-27, 33-46, 51-60, 81-126 |
| src/face\_analyzer/detectors/scrfd.py         |       58 |       47 |       14 |        1 |     17% |20-24, 45-111 |
| src/face\_analyzer/detectors/ssd.py           |       35 |        1 |       10 |        1 |     96% |        19 |
| src/face\_analyzer/detectors/yolo.py          |       61 |       51 |       10 |        1 |     15% |21-31, 36-37, 46-100 |
| src/face\_analyzer/fusion/ensembles.py        |       29 |        2 |       14 |        3 |     88% |37-\>35, 50, 55 |
| src/face\_analyzer/gallery/database.py        |       55 |        5 |       18 |        5 |     86% |37-\>58, 46, 56-57, 59, 64, 70-\>76 |
| src/face\_analyzer/gallery/eigenfaces.py      |       66 |        6 |       16 |        5 |     87% |32-\>47, 35, 38-39, 42, 44, 105 |
| src/face\_analyzer/gallery/search.py          |      148 |       57 |       52 |        4 |     60% |36-40, 74, 90-94, 99-110, 116-147, 164, 192, 209-211, 225, 232, 242 |
| src/face\_analyzer/inference.py               |       15 |        1 |        0 |        0 |     93% |       113 |
| src/face\_analyzer/liveness.py                |      100 |        6 |       32 |        7 |     90% |55-\>53, 63-\>61, 75, 77, 81, 93, 162-\>168, 176-177 |
| src/face\_analyzer/pipeline/analyzer.py       |       35 |        1 |       12 |        1 |     96% |        63 |
| src/face\_analyzer/pipeline/cache.py          |       35 |        1 |        8 |        1 |     95% |        63 |
| src/face\_analyzer/pipeline/drawing.py        |       62 |        6 |       12 |        0 |     92% |22-24, 34-35, 42 |
| src/face\_analyzer/pipeline/face\_tasks.py    |      213 |       73 |       84 |       20 |     61% |105, 108-113, 130-\>132, 136-\>148, 138-147, 162, 187-\>191, 189, 209, 212, 216, 222, 249, 278-284, 294-296, 318-336, 344-352, 360-368, 379-390, 398-406 |
| src/face\_analyzer/pipeline/landmarks.py      |       69 |       53 |       16 |        2 |     21% |14, 19-23, 30-36, 50, 58-95, 102-135 |
| src/face\_analyzer/pipeline/loader.py         |      190 |       70 |       80 |       23 |     60% |57-58, 65-69, 76, 83, 91-92, 101, 108, 164, 172, 196, 198, 204, 211, 219, 223, 226-237, 245-249, 255-257, 259, 263, 267-271, 275, 281, 298-313, 321, 329, 338-349, 357-365, 377-380, 388 |
| src/face\_analyzer/pipeline/stages.py         |      150 |       15 |       40 |       11 |     83% |98, 145-155, 162-\>164, 227, 257-\>264, 261-\>264, 277, 286-296, 341, 363, 399-403 |
| src/face\_analyzer/pipeline/tracker.py        |       63 |        1 |       20 |        1 |     98% |        64 |
| src/face\_analyzer/ui/adjustments.py          |       21 |       16 |       12 |        0 |     15% |12-18, 23-39 |
| src/face\_analyzer/ui/live.py                 |      139 |       83 |       38 |        1 |     32% |104-112, 152, 158, 165, 178-338 |
| src/face\_analyzer/ui/results.py              |      306 |      116 |      118 |       26 |     56% |53, 182, 209, 216-225, 238, 245-246, 254-257, 269-282, 287, 297-314, 317-319, 386, 388, 391-400, 414-\>425, 426-437, 460, 491-519, 524-\>526, 546-549, 559, 575-611, 616, 626-633, 653-\>687, 665-685, 688-703, 712-750 |
| src/face\_analyzer/ui/share\_card.py          |       58 |        1 |        6 |        2 |     95% |45, 86-\>94 |
| src/face\_analyzer/ui/sidebar.py              |      123 |       13 |       34 |        9 |     83% |54-\>56, 79, 147-\>157, 164, 226, 265-\>267, 268-273, 298-300, 314 |
| **TOTAL**                                     | **3176** |  **987** |  **902** |  **151** | **65%** |           |

14 files skipped due to complete coverage.


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/dpologdvinity/multimodel-face-analyzer/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/dpologdvinity/multimodel-face-analyzer/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/dpologdvinity/multimodel-face-analyzer/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/dpologdvinity/multimodel-face-analyzer/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fdpologdvinity%2Fmultimodel-face-analyzer%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/dpologdvinity/multimodel-face-analyzer/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.