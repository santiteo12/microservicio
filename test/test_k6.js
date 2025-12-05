// test_k6.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 10, // usuarios virtuales
  duration: '20s', // duración total
};

export default function () {
  // Cambia el ID si quieres probar otros alumnos
  const res = http.get('http://localhost:5002/api/v1/certificado/1/test');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'no error field': (r) => !r.json().error,
    'tiene nombre': (r) => r.json().nombre !== undefined,
    'tiene especialidad': (r) => r.json().especialidad !== undefined,
  });
  sleep(1);
}