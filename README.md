# Covid-19 impact

This repository is intended to be descriptive for the analysis of two related subjects about covid-19.

These subjects are the followings:
* Study case 1:

Wich refers to the study of the behavior of the covid-19 interest over time and how the people interest in online courses, and even learning attitudes vary with respect of covid-19 interest.

* Study case 2:

To study some of the epidemiological data of the covid-19, Colombia was chosen as country of study. To carry out this, a model of the cases was made to see the impact of obligated quarantine (decreed on 2020-03-24) and selective isolation (started at 2020-09-01). Also how this has affected the deparments of this country.
In the end a shallow analysis is done to see the impact of some other variables with respect to the epidmilogical variables.


## What does this repo have?

This repository is separated in three parts as following:
* _/notebooks_
* _/src_
* _/API_

Every folder has its own README to get some sense of them, for now they will be described shortly.

### **_/notebooks_**

This folder has the jupyter notebooks where the analysis of the study cases where made.

### **_/src_**

This folder is intended to be use when the repository receives a push, so that github actions can plot the status and the performance of the model built in previous described folder. By default it takes Colombia data.

### **_/API_**

Source code of the API service that has the model built in notebooks analysis on a production environment, so that it can be used as a service by anyone.

## Licensing

This repository is under a MIT License.

## Data

Data was obtained by conecting to google trends and using Google's COVID-19 Open-Data.

## Citations

Google's COVID-19 Open-Data
```
@article{Wahltinez2020,
  author = "O. Wahltinez and others",
  year = 2020,
  title = "COVID-19 Open-Data: curating a fine-grained, global-scale data repository for SARS-CoV-2",
  note = "Work in progress",
  url = {https://goo.gle/covid-19-open-data},
}
```






