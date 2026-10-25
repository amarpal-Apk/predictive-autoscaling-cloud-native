import http from 'k6/http';
import { check } from 'k6';

export const options = {
  scenarios: {
    periodic_traffic: {
      executor: 'ramping-arrival-rate',
      startRate: 3,
      timeUnit: '1s',
      preAllocatedVUs: 10,
      maxVUs: 25,
      stages: [
        { duration: '30s', target: 3 },
        { duration: '30s', target: 15 },
        { duration: '30s', target: 3 },
        { duration: '30s', target: 15 },
        { duration: '30s', target: 3 },
        { duration: '30s', target: 15 },
      ],
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
