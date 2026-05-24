pipeline {
    agent any  // Используем любой доступный агент

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

        stage('Setup Python Environment') {
            steps {
                script {
                    // Проверяем, что Python 3.11 установлен
            sh 'python3.11 --version || python --version'

            // Создаём виртуальное окружение
            sh 'python3.11 -m venv venv || python -m venv venv'
            sh 'source venv/bin/activate'

            // Устанавливаем зависимости
            sh 'pip install --no-cache-dir -r requirements.txt'
            sh 'playwright install chromium'
        }
    }
}

        stage('Run All Tests') {
            options {
                timeout(time: 30, unit: 'MINUTES')  // Тайм‑аут 30 минут
            }
            steps {
                script {
                    try {
                        sh '''
                            mkdir -p allure-results reports
                            if [ -d "test/hirehi/tests" ]; then
                                source venv/bin/activate
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
                throw e
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