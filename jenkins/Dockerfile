FROM jenkins/jenkins:lts

USER root
RUN apt-get update && apt-get install -y docker.io ca-certificates curl gnupg \
    && rm -rf /var/lib/apt/lists/*

# Let the jenkins user talk to Docker
RUN usermod -aG docker jenkins

USER jenkins

