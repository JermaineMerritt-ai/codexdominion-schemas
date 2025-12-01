"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
// pages/capsules-simple.tsx
var dynamic_1 = require("next/dynamic");
var Capsules = (0, dynamic_1.default)(function () { return Promise.resolve().then(function () { return require('../components/CapsulesSimple'); }); }, {
    ssr: false,
});
exports.default = Capsules;
