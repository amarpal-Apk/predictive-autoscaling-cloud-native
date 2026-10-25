import http from 'k6/http';
import { check } from 'k6';

export const options = {
  scenarios: {
    constant_traffic: {
      executor: 'constant-arrival-rate',
      rate: 5,
      timeUnit: '1s',
      duration: '2m',
      preAllocatedVUs: 10,
      maxVUs: 20,
    },
  },
};

export default function () {
  const url = `${__ENV.BASE_URL || 'http://host.docker.internal:8080'}/api/test`;
  const res = http.get(url);

  check(res, {
    'status is 200': (r) => r.status === 200,
  });
}
