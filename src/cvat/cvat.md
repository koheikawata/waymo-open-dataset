## Set up CVAT
```
echo 'export PATH="$PATH:/mnt/c/Program Files/Docker/Docker/resources/bin:/mnt/c/ProgramData/DockerDesktop/version-bin"' >> ~/.profile
tail ~/.profile

git clone https://github.com/opencv/cvat
cd cvat

sudo docker-compose up -d
```

```
cd $PWD
docker-compose down
```

```
docker exec -it cvat bash -ic 'python3 ~/manage.py createsuperuser'
```

```
docker-compose -f docker-compose.yml -f components/serverless/docker-compose.serverless.yml up -d
docker-compose -f docker-compose.yml -f components/serverless/docker-compose.serverless.yml down
```

## Find models
```
find . -name "function.yaml"
```

Example of output
```
./serverless/openvino/dextr/nuclio/function.yaml
./serverless/openvino/omz/intel/person-reidentification-retail-300/nuclio/function.yaml
./serverless/openvino/omz/intel/semantic-segmentation-adas-0001/nuclio/function.yaml
./serverless/openvino/omz/intel/text-detection-0004/nuclio/function.yaml
./serverless/openvino/omz/public/faster_rcnn_inception_v2_coco/nuclio/function.yaml
./serverless/openvino/omz/public/mask_rcnn_inception_resnet_v2_atrous_coco/nuclio/function.yaml
./serverless/openvino/omz/public/yolo-v3-tf/nuclio/function.yaml
./serverless/pytorch/foolwood/siammask/nuclio/function.yaml
./serverless/pytorch/saic-vul/fbrs/nuclio/function.yaml
./serverless/pytorch/shiyinzhang/iog/nuclio/function.yaml
./serverless/tensorflow/faster_rcnn_inception_v2_coco/nuclio/function.yaml
./serverless/tensorflow/matterport/mask_rcnn/nuclio/function.yaml
```
