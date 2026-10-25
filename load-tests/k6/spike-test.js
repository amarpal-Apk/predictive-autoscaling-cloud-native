import http from 'k6/http';
import { check } from 'k6';

export const options = {
  scenarios: {
    spike_test: {
      executor: 'ramping-arrival-rate',
      startRate: 5,
      timeUnit: '1s',
      preAllocatedVUs: 15,
      maxVUs: 30,
      stages: [
        { duration: '30s', target: 5 },
        { duration: '10s', target: 25 },
        { duration: '30s', target: 25 },
        { duration: '10s', target: 5 },
        { duration: '30s', target: 5 },
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
