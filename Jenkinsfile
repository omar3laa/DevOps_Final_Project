pipeline {
    agent any

    environment {
        // حط هنا رابط المستودع الجديد الخاص بمشروع الأرقام
        REPO_URL = 'https://github.com/omar3laa/DevOps_Final_Project' 
        BRANCH = 'main'
        GIT_CREDENTIALS_ID = 'GitCred'
        SCANNER_HOME = tool 'sonar_server'
    }

    stages {
        stage('Checkout Code') {
            steps {
                // سحب الكود من مستودعك
                git branch: "${BRANCH}", credentialsId: "${GIT_CREDENTIALS_ID}", url: "${REPO_URL}"
            }
        }

        stage('SonarQube Analysis') {
            steps {
                // تم تعديل الـ ProjectKey والـ ProjectName ليناسب المشروع الحالي
                withSonarQubeEnv('sonar_server') {
                    sh "${SCANNER_HOME}/bin/sonar-scanner -Dsonar.projectKey=Digit_Recognition -Dsonar.projectName='Digit_Recognition' -Dsonar.sources=."
                }
            }
        }
        
        stage('Deploy with Docker Compose') {
            steps {
                sh '''
                docker compose down -v || true
                docker compose up -d --build
                 '''
            }
        }
    }
    post {
        success {
            echo '✅ Deployment Successful! The application is running on port 18099.'
        }
        failure {
            echo '❌ Pipeline failed! Please check the logs.'
        }
    }
}
