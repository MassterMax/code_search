hello_world:
	@echo "Hello world!!"

# todo - add make testenv with elastic docker

dockerd:
	sudo dockerd

#test_env:
# docker pull docker.elastic.co/elasticsearch/elasticsearch:7.16.0
	#sudo docker run --memory="500m" --memory-reservation="250m" -p 127.0.0.1:9200:9200 -p 127.0.0.1:9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.16.0

#killall:
#	kill -9 -1
#	wsl --shutdown