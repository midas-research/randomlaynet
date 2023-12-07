# RanLayNet: A Dataset for Document Layout Detection used for Domain Adaptation and Generalization

## INTRODUCTION

* Current layout detection datasets for deep learning lack diversity, necessitating a large number of annotated instances for training, resulting in high costs and time demands.
* Proposing RanLayNet, a synthetic document dataset with auto-assigned labels for layout elements, addressing challenges by offering a versatile dataset for robust model training across diverse document formats.
* Developed domain adaptation for layout identification using limited labeled data, improving a deep model trained on RanLayNet compared to models using only real documents.

## MOTIVATION AND CHALLENGES
* The limited diversity of layouts in Public datasets [1] [2]  necessitates many annotated instances.
* Annotating enough instances for training is costly and time-consuming.
* Differences between source (training data) and target (real-world application) domains can greatly affect model performance.

## OUR SOLUTION
* Introduced RanLayNet, a synthetic document dataset.
* Dataset enriched with labels for spatial positions, ranges, and types of layout elements.
* Aim to create a dataset for training models adaptable and robust to various document formats.

## DATASET (RanLayNet)
* The dataset includes diverse layout classes, ensuring balanced representation and enhancing model’s ability to handle real-world layouts effectively.
* Deep learning models trained on RanLayNet provide insights into document layout, including spatial positions, extents, and element categories. Exposure to diverse layouts enhances their adaptability to real-world variations.
* RanLayNet's versatility enables training models for diverse layouts, effectively handling domain shifts in document structures. Models trained on RanLayNet outperform PublayNet models, showcasing robustness and adaptability to various layouts, reinforcing domain adaptation.

## METHODOLOGY FOR RANLAYNET DATASET GENERATION 

![MarineGEO circle logo](/assets/img/MarineGEO_logo.png "MarineGEO logo")



