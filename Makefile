extract_data:
	cd codesearch/preproc && python3 -m load_data && cd ../..

test_env_daemon:
	sudo dockerd

test_env_download:
	docker pull docker.elastic.co/elasticsearch/elasticsearch:7.16.0

test_env_up:
	sudo docker run -d --name elasticsearch --memory="500m" --memory-reservation="250m" -p 127.0.0.1:9200:9200 -p 127.0.0.1:9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.16.0

test_env_stop:
	sudo docker stop elasticsearch

test_env_resume:
	sudo docker start elasticsearch
