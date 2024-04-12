# How Composable is the Web?

## Introduction
An attempt at replicating the findings of S. Serbout, C. Pautasso and U. Zdun, "How Composable is the Web? An Empirical Study on OpenAPI Data model Compatibility," 2022 IEEE International Conference on Web Services (ICWS), Barcelona, Spain, 2022, pp. 415-424, doi: 10.1109/ICWS55610.2022.00068.
<br>
<b>Link to the paper:</b> [How Composable is the Web? An Empirical Study on OpenAPI Data model Compatibility](https://ieeexplore.ieee.org/document/9885779)
<br>
Implementation instructions are included in the pdf Report included in the repository along with our analysis.

### Repository Authors
1. Archit Joshi (aj6082@rit.edu)
2. Athina Stewart (as1896@rit.edu)
3. Chung-An Huang (ch1949@rit.edu)


### Script Overview
1. [cleanDataSet.py](cleanDataSet.py): This script is used to clean the dataset with over 71,415 API descriptions as per the standards mentioned in the paper. The script also has endpoints to a MongoDB cluster which will store the extracted parameters from the cleaned data.
2. [extractMethodParameters.py](extractMethodParameters.py): This script is used to extract the GET and POST method parameters from the cleaned dataset. The "unified representation" is returned to cleanDataSet.py from where its stored in the database.
3. [count_endpoints.py](count_endpoints.py): This script is used to count the number of endpoint matches in the new API representations stored in the dataset.
4. [data_type_match.py](data_type_match.py): This script is used to perform data-type matching of the parameters in the new API representations stored in the dataset.
5. [property_name_match.py](property_name_match.py): This script is used to perform property-matchin for the new API representations stored in the dataset.
6. [perform_experiment_from_paper.py](perform_experiment_from_paper.py): This script is used to perform the experiment as mentioned in the paper. It uses the above scripts to perform the experiment.
7. [validate_schema_object.py](validate_schema_object.py): This script serves as our previsualization of data. We try to impose the stringent checks mentioned in the paper by the authors.
8. [test_attribute_probability_in_schema.py](test_attribute_probability_in_schema.py) : This script is another previsualization of data before cleaning it. Based on the outcomes of scripts 7 & 8 we adapted our cleaning process to address the fact that we lack the original dataset and performing the stringent checks would greatly compromise the data samples we work with during the experiment based on APIGurus dataset which is significantly smaller than what the authors use originally.
