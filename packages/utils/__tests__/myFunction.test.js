"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var myFunction_1 = require("../src/myFunction");
describe('myFunction', function () {
    it('should return a greeting message', function () {
        expect((0, myFunction_1.myFunction)('Jermaine')).toBe('Hello, Jermaine! Welcome to CodexDominion.');
    });
});
