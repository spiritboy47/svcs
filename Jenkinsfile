pipeline {
    agent any

    environment {
        PROJECT_DIR = "/home/ubuntu/svcs"
    }

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Make deploy script executable') {
            steps {
                sh '''
                    chmod +x deploy.sh
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    ./deploy.sh
                '''
            }
        }
    }

    post {
        success {
            echo "Deployment successful ✅"
        }

        failure {
            echo "Deployment failed ❌ (rollback should have executed inside deploy.sh)"
        }

        always {
            echo "Cleaning workspace..."
            cleanWs()
        }
    }
}
