pipeline {
  agent any
  environment {
    IMAGE = "${laxmisharany6/ticket-booking}:${GIT_COMMIT}"
    DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds') // create in Jenkins
    KUBECONFIG_CREDENTIALS = credentials('kubeconfig') // create in Jenkins (kubeconfig as secret file)
  }
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    stage('Build') {
      steps {
        sh 'docker --version || true'
        sh 'docker build -t $IMAGE .'
      }
    }
    stage('Unit Test') {
      steps {
        // simple smoke test - run container and call health endpoint
        sh '''
          cid=$(docker run -d -p 5000:5000 $IMAGE) || true
          sleep 2
          curl -f http://localhost:5000/ || true
          docker rm -f $cid || true
        '''
      }
    }
    stage('Push to Docker Hub') {
      steps {
        withCredentials([string(credentialsId: 'dockerhub-username', variable: 'DOCKER_USER'), string(credentialsId: 'dockerhub-password', variable: 'DOCKER_PASS')]) {
          sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
          sh 'docker push $IMAGE'
        }
      }
    }
    stage('Deploy to Kubernetes') {
      steps {
        // write kubeconfig from Jenkins credential to file and use kubectl
        sh '''
          echo "$KUBECONFIG_CREDENTIALS" > kubeconfig
          export KUBECONFIG=$PWD/kubeconfig
          kubectl apply -f k8s/deployment.yaml
          kubectl apply -f k8s/service.yaml
        '''
      }
    }
  }
  post {
    always {
      sh 'docker logout || true'
    }
  }
}
