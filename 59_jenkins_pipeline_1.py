59_jenkins_pipeline_1

pipeline {
  agent any
  tools {
    maven 'Maven 3.6.3'
  }
  stages {
    stage("Build") {
      steps {
        script {
          try {
            sh "mvn --version"
          } catch (Exception e) {
            error("Maven is not available, please install Maven and ensure it is in the PATH.")
          }
        }
        script {
          if (fileExists('xxx')) {
            dir('xxx') {
              sh "git fetch --all"
              sh "git checkout master" 
              sh "git reset --hard origin/master" 
            }
          } else {
            sh "git clone -b master http://xxx:8080/xxx/xxx.git" 
          }
        }
        dir('xxx') {
          sh "mvn clean install"
        }
      }
    }
    stage("Deploy") {
      steps {
        //sh "pwd"
        sh "scp -P60022 /var/lib/jenkins/workspace/xxx/xxx/xxx/target/xxx.jar 172.16.228.88:/home/java/jenkins_upload/"
        sh "scp -P60022 /var/lib/jenkins/workspace/xxx/xxx/xxx/target/xxx.jar 172.16.228.88:/home/java/jenkins_upload/" 
      }
    }
  }
}

