# LATTE connector

LATTE connector is a Virtual Python Environment that connects the LATTE web application to powerfull Python models to recognize entities and return them to the user. This manual assumes Python is installed on your machine and that you hava access to PowerShell/Terminal. 

## Installation
- Requires an active Python installation. 
- Download the LATTE connector to a folder on the same machine you run the LATTE web app.
- Install a virtual environment in a dedicated folder by using from a PowerShell window: 
    `python -m venv . `
- Activate this new virtual environment by typin `.\Scripts\activate` from within the same PowerShell window. The name of the folder you're in should show up in PowerShell.
- In this folder copy the content you downloaded from the GitHub page. 
- Install all required modules from the requirements.txt file. 
    ```
    pip install -r requirements.txt
    ```
- You'll need to remember where you installed the Python application. The full path to python.exe and the hostfiles folder is required for LATTE

## Configuration
The LATTE connector does not require further configuration, but the LATTE web app needs to know the connector is installed and where it is located. For this it is important that you pass thedirectory of the LATTE connector and the exact location of the python-executable of the LATTE connector to the LATTE web app using the LATTE config.inc.php config file. 

### Configuring the LATTE Web App
The config.inc.php file of the LATTE Web App needs to know the location of the python executable and LATTE connector directory. You also need to explicitly instruct it to use the LATTE connector. 
This part of the LATTE Web App is configured in the config.inc.php file under the section ```########### LATTE CONNECTOR INTEGRATION: ###########````
- To enable the use of the LATTE Connector, you have to set the `$use_connector` variable to True.
- If this is set to True, the configuration needs to be passed down too. The `$pyenv` variable should hold the path to the Python executable. 
- The `$scripts` variable needs to have the full absolute path to the hostfiles subfolder of the virtual environment. 
- The `$languageDetectionEngine` variable needs to be set to the name of the language detection engine. Currently, only `langid.py` is supported. 

Notes: 
The directory is the place where you installed the virtual environment, it contains the config.ini file needed to load additional LLM's, and the hostfiles subdirectory where the entity extractor scripts are located. You need to pass the absolute path to this hostfiles subdirectory directory to the LATTE Web App in the config.inc.php file 

Your Python executable of the virtual environment is located in the **Scripts** subdirectory of the directory where you installed your virtual environment to. You need to pass the absolute path to this executable to the LATTE Web App. 



## Extending
To identify a language, LATTE connector uses [langid.py](https://github.com/saffsd/langid.py), which can quickly identify 97 languages. The identified language is returned by it's ISO 639-1 identifier. 


The LATTE connector can be extended by adding additional Spacy LLM pipeplines as long as langid.py is capable of recognizing the language. Currently the LATTE connector comes with the following pipelines installed: 

|Language | ISOcode (639-1)  | Model |
|---------|---------|-------|
|German   | de      | [de_core_news_md (V3.7.0) ](https://spacy.io/models/de#de_core_news_md) |
|Greek    | el      | [el_core_news_md (V3.7.0) ](https://spacy.io/models/el#el_core_news_md) |
|English  | en      | [en_core_web_lg (V3.7.1)](https://spacy.io/models/en#en_core_web_lg) |
|French  | fr      | [fr_core_news_md (V3.7.0)](https://spacy.io/models/fr#fr_core_news_md) |
|Dutch  | nl      | [nl_core_news_md (V3.7.0)](https://spacy.io/models/nl#nl_core_news_md) |
|---------|---------|-------|
  
Additional models can be downloaded from the [Spacy homepage](https://spacy.io/models/) and shoud be installed to the LATTE connector virtual environment. A model is suited to be used by the LATTE connector if it has the **NER** tag available in the Componenents and Pipeline section of a model's release details. 

Once the model is installed, you have to add it as a key-value pair to the `config.ini` file under the `Models` section. 

e.g. Let's assume we want to install the it_core_news_md model to perform NER in Italian texts: 
1) Verify the model has an NER component by reading the documentation
2) If the suitability is verified, open PowerShell and use the following abstracted command: 
```<full path to python.exe from the LATTE connector virtual environment> -m spacy download <packagename>```
Assuming our python executable of the Latte connector virtual environment is located at: 'C:/Workdir/MyApps/Python_VENV/LATTE_connector/Scripts/python.exe' and our package is named 'it_core_news_md', the command becomes: 
```C:/Workdir/MyApps/Python_VENV/LATTE_connector/Scripts/python.exe -m spacy download it_core_news_md```
3) Once the installation is completed opent the `config.ini` file and extend the `Models` section with a new key-value pair. The key should be the ISO code of the language the model is trained on and the value should be the name of the model. The key and the value should not be quoted. You can override the default models by other ones simply by reusinig the key. 
In this example we add the following line to the `config.ini` file: 

```
[Models]
it = it_core_news_md
```
example with multiple models: 
```
[Models]
it =it_core_news_md 
eg = examplegivenmodel
ex3 = example3

```