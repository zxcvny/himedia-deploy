// 배포 버전의 FastAPI 주소 또는 로컬 FastAPI 주소를 받아오는 함수
const getAPIBaseURL = () => {
    // Endpoint 직전 주소 (BaseURL)

    // render에 배포할 때 환경 변수에 접근하면 HOST 이름만 리턴한다.
    const fastApiHost = import.meta.env.VITE_FASTAPI_HOST;

    if (fastApiHost.startsWith('http')) {
        // 로컬 환경 ex) http://localhost:8000
        return fastApiHost;
    }

    // render의 web service의 도메인은
    // https://{host_name}.onrender.com
    // ex) https://fastapi-ddddd.onrender.com
    // 이것이 리턴되면 App.jsx에서 배포된 FastAPI 서버로 요청할 수 있음
    return `https://${fastApiHost}.onrender.com`;
}

export const API_BASE_URL = getAPIBaseURL();