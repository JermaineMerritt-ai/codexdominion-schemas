import { myFunction } from '../src/myFunction';

describe('myFunction', () => {
  it('should return a greeting message', () => {
    expect(myFunction('Jermaine')).toBe('Hello, Jermaine! Welcome to CodexDominion.');
  });
});
