# *SDE* Online Assessment

**Run Dockerfile by using** 

`docker build sde-test <Dockerfile_path>`



**upload input.json to /submission directory** 

Start using the docker by using

`docker run -i -t -v /submission/:/submission/ sde-test input.json output.json`

The output.json file will generate in /submission
