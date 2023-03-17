# 현재까지 결과
![image](https://user-images.githubusercontent.com/70372577/223656679-969f529c-4b70-4673-9914-7cf8aba6e151.png)

( requests 설치시 error가 지속적으로 나와서 kivy에서 지원하는 UrlRequest 사용하였음 -> 서버전송가능 )

( UrlRequest는 자료가 너무없어서 requests로 그냥 시도..! )




# 사용방법

(앱에서 로드하려면 ubuntu에서 buildozer 설치해야 합니다.)
main.py에 kivy앱을 개발, buildozer.spec에서 앱 이름 및 세부사항을 조절하여 
buildozer android debug deploy run
실행!


또한 라이브러리가 제대로 설치안되어있으면, 어플이 실행하자말자 종료될 수 있다.
따라서 추가적인 라이브러리가 있다면 buildozer.spec에 requirements에 라이브러리를 추가해주어야한다.


또한 카메라 사용시
        try:
            # permission을 해줘야해서 무조건 있어야합니다..!
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.CAMERA,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE
            ])
        except:
            pass



그리고 앱에서 꺼진거 로그보려면 adb 설치하고
adb logcat 하면 어떤 이유로 error가 도출되었는지 표출 됨.


# buildozer.spec의 requirements 

requests 사용시 해당버전 사용할것.

requirements = python3, kivy==2.0.0rc4, kivymd==0.102.1, requests, urllib3, chardet, certifi, idna로 해야합니다. -> requests 모듈 사용시 에러가 나는데, 어떤분이 공유해주셨네요.
