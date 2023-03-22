docker rm -f discord
docker run -d --name discord \
       -v "$PWD/src:/gpt-discord-bot/" \
       -v "$PWD/logs:/logs/" \
       -it gpt-discord-bots
docker logs discord -f

# docker rm -f discord
# docker run -v "$PWD/src:/gpt-discord-bot/" -d \
#         --name discord -it gpt-discord-bots
# docker logs discord -f
