import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

const errorRate = new Rate('request_errors');

export const options = {
  stages: [
    { duration: '30s', target: 5 },
    { duration: '1m', target: 10 },
    { duration: '1m', target: 20 },
    { duration: '30s', target: 0 },
  ],

  thresholds: {
    http_req_failed: ['rate<0.05'],
    http_req_duration: ['p(95)<1000'],
    request_errors: ['rate<0.05'],
  },
};

export default function () {
  const baseUrl = __ENV.BASE_URL || 'http://host.docker.internal:8080';

  const response = http.get(`${baseUrl}/api/test`);

  const passed = check(response, {
    'status is 200': (r) => r.status === 200,
  });

  errorRate.add(!passed);

  sleep(1);
}
