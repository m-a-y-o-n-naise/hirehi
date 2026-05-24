pipeline {
    agent {
        docker {
            image 'python:3.11-slim'  // обновлённая версия Python
            args '-u 0:0'  // запуск от root для установки браузеров
        }
    }

    environment {
        PLAYWRIGHT_BROWSERS_PATH = '/tmp/playwright'  // кэширование браузеров
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/m-a-y-o-n-naise/hirehi'  // клон из гита
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install --no-cache-dir -r requirements.txt'
                sh 'playwright install chromium'
            }
        }

        stage('Run All Tests') {
            steps {
                script {
                    try {
                        sh '''
                            mkdir -p allure-results reports
                            pytest test/hirehi/tests/ \
                                --alluredir=allure-results \
                                --html=reports/test-report.html \
                                --self-contained-html \
                                -n auto
                '''
            } catch (e) {
                echo "Некоторые тесты провалились, продолжаем выполнение"
                throw e  // чтобы пайплайн отметился как неудачный
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