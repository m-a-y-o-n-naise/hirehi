pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '-u 0:0'
        }
    }

    environment {
        PLAYWRIGHT_BROWSERS_PATH = '/tmp/playwright'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/m-a-y-o-n-naise/hirehi'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install --no-cache-dir -r requirements.txt'
                sh 'playwright install chromium || exit 1'  // прерываем пайплайн при ошибке установки
            }
        }

        stage('Run All Tests') {
            options {
                timeout(time: 30, unit: 'MINUTES')  // тайм‑аут 30 минут
            }
            steps {
                script {
                    try {
                        sh '''
                            mkdir -p allure-results reports
                            if [ -d "test/hirehi/tests" ]; then
                        pytest test/hirehi/tests/ \
                            --alluredir=allure-results \
                            --html=reports/test-report.html \
                            --self-contained-html \
                            -n auto
            else
                echo "Ошибка: директория test/hirehi/tests не найдена!"
                exit 1
            fi
        '''
            } catch (e) {
                echo "Тесты завершились с ошибками: ${e.getMessage()}"
                throw e  // прерываем пайплайн при ошибке
            }
        }
    }
}

        stage('Generate Allure Report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    properties: [],
                    reportBuildPolicy: 'ALWAYS'
                ])
            }
        }

        stage('Publish Test Reports') {
            steps {
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
            reportFiles: 'test-report.html',
            reportName: 'HTML Test Report'
                ])
            }
        }
    }

    post {
        success {
            echo 'Все тесты успешно выполнены!'
            slackSend(
                channel: '#testing',
                message: "✅ Автотесты успешно завершены: ${env.BUILD_URL}"
            )
        }
        failure {
            echo 'Тесты завершились с ошибками!'
            slackSend(
                channel: '#testing',
                message: "❌ Ошибки в автотестах: ${env.BUILD_URL}"
            )
        }
        always {
            cleanWs()
        }
    }
}