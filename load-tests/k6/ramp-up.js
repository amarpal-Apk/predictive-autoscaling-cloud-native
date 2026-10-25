import http from 'k6/http';
import { check } from 'k6';

export const options = {
  scenarios: {
    ramp_up: {
      executor: 'ramping-arrival-rate',
      startRate: 2,
      timeUnit: '1s',
      preAllocatedVUs: 10,
      maxVUs: 25,
      stages: [
        { duration: '30s', target: 5 },
        { duration: '30s', target: 10 },
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
