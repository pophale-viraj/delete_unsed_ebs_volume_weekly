pipeline {
    agent any
    environment {
        AWS_REGION = 'us-east-1' // Set default region
    }
    stages {
        stage('Checkout') {
            steps {
                // Clone your repository containing the Python script
                checkout scm
            }
        }
        stage('Install Dependencies') {
            steps {
                script {
                    // Install Python and Boto3 if not already installed
                    sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install boto3
                    '''
                }
            }
        }
        stage('Run Cleanup Script') {
            steps {
                script {
                    // Execute the Python script
                    sh '''
                    source venv/bin/activate
                    python3 cleanup_old_unattached_ebs.py
                    '''
                }
            }
        }
    }
    post {
        always {
            // Clean up the virtual environment
            sh 'rm -rf venv'
        }
    }
}
