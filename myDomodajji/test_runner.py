# 유닛 테스트시 테스트 DB가 아닌 내가 설정한 DB로 테스트 할 수 있게 하는 파일 

# DiscoverRunner : 테스트 DB 생성 담당 클래스 
from django.test.runner import DiscoverRunner

# 장고 유닛테스트에서 사용되는 runner를 재정의한 클래스 
# 밑의 기존 메서드들을 재정의하여 비어두면, 
# 테스트시 테스트 DB 생성 없이 테스트 가능 
class TestRunner(DiscoverRunner):

    def setup_databases(self, **kwargs):
        pass
    
    def teardown_databases(self, old_config, **kwargs):
        pass