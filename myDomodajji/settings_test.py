# 기본 settings.py의 모든 내용을 가져온 후, 테스트를 teest_runner.py로 하라고 알려주는 파일

# settings.py의 모든 항목 불러오기 
from myDomodajji.settings import *

# test_runner.py에서 정의한 TestRunner 클래스를 테스트 러너로 지정
TEST_RUNNER = 'myDomodajji.test_runner.TestRunner'

# 테스트 실행 명령어 
# [1] python manage.py test users --settings='myDomodajji.settings_test'
# [2] python manage.py test users --testrunner='myDomodajji.test_runner.TestRunner'