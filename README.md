# GitHub action for installing libraries to  Databricks clusters

This is a github action that will install custom libraries to Databricks clusters. The libraries need to be stored in DBFS path. 

The implement of this action is based on the code and example in [Continuous integration and delivery on Databricks using Jenkins](https://docs.databricks.com/dev-tools/ci-cd/ci-cd-jenkins.html) 

Here is a action workflow example.  

```yaml
name: Run Databicks Notebooks GitHub Install Library Action Demo 
on: 
  push:
    branches: 
      - master 
jobs:
  build-and-deploy: 
    runs-on: ubuntu-latest
    steps:
    - name: Checkout
      uses: actions/checkout@master
    - name: Install WHL to the cluster
      uses: Herman-Wu/databrick-install-lib-action@master
      with:
        databrick-server-uri: 'https://XXXX.XX.azuredatabricks.net'
        databrick-token: ' <databrick-token> '
        databrick-cluster-id: ' < databrick-cluster-id >'
        databrick-libraries: ' XXXX.whl  YYYY.whl ZZZ.whl'
        databrick-dbfs-path: 'dbfs:/mnt/XXXX/ '
```


<br>

**Future Improvement**
    - improve docker image preparation time