"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var ConstellationAscii = function (_a) {
    var _b = _a.showAnimation, showAnimation = _b === void 0 ? true : _b, _c = _a.size, size = _c === void 0 ? 'medium' : _c, _d = _a.theme, theme = _d === void 0 ? 'golden' : _d;
    var sizeClasses = {
        small: 'text-xs',
        medium: 'text-sm',
        large: 'text-base',
    };
    var themeClasses = {
        golden: {
            central: 'text-yellow-400',
            lines: 'text-yellow-500',
            domains: {
                storefront: 'text-emerald-400',
                personal: 'text-yellow-400',
                educational: 'text-green-400',
                experimental: 'text-orange-400',
                council: 'text-blue-400',
                premium: 'text-purple-400',
            },
        },
        purple: {
            central: 'text-purple-400',
            lines: 'text-purple-500',
            domains: {
                storefront: 'text-cyan-400',
                personal: 'text-indigo-400',
                educational: 'text-teal-400',
                experimental: 'text-pink-400',
                council: 'text-violet-400',
                premium: 'text-fuchsia-400',
            },
        },
        rainbow: {
            central: 'text-yellow-400',
            lines: 'text-gradient-rainbow',
            domains: {
                storefront: 'text-red-400',
                personal: 'text-yellow-400',
                educational: 'text-green-400',
                experimental: 'text-orange-400',
                council: 'text-blue-400',
                premium: 'text-purple-400',
            },
        },
    };
    var currentTheme = themeClasses[theme];
    return (<div className={"font-mono ".concat(sizeClasses[size], " text-center relative overflow-x-auto")}>
      {/* Central Crown */}
      <div className="mb-4">
        <div className={"".concat(currentTheme.central, " font-bold ").concat(showAnimation ? 'animate-pulse' : '')}>
          ✨ Codexdominion.app ✨
        </div>
        <div className="text-xs text-gray-400 italic mt-1">(Ceremonial Crown — Codex Bulletin)</div>
      </div>

      {/* Connection Tree */}
      <div className={"".concat(currentTheme.lines, " mb-6 ").concat(showAnimation ? 'animate-pulse' : '')}>
        <pre className="leading-tight whitespace-pre">
          {"                               /     |     \\\n                              /      |      \\\n                             /       |       \\\n                            /        |        \\\n                           /         |         \\\n                          /          |          \\\n                         /           |           \\\n                        /            |            \\\n                       /             |             \\\n                      /              |              \\\n                     /               |               \\\n                    /                |                \\\n                   /                 |                 \\\n                  /                  |                  \\\n                 /                   |                   \\\n                /                    |                    \\\n               /                     |                     \\\n              /                      |                      \\\n             /                       |                       \\\n            /                        |                        \\\n           /                         |                         \\\n          /                          |                          \\\n         /                           |                           \\\n        /                            |                            \\\n       /                             |                             \\\n      /                              |                              \\\n     /                               |                               \\\n    /                                |                                \\\n   /                                 |                                 \\\n  /                                  |                                  \\\n /                                   |                                   \\\n/                                    |                                    \\"}
        </pre>
      </div>

      {/* Domain Crowns */}
      <div className="grid md:grid-cols-3 gap-4 text-xs">
        {/* Left Column */}
        <div className="space-y-2">
          <div className={"".concat(currentTheme.domains.storefront, " font-bold")}>🛍️ aistorelab.com</div>
          <div className={"".concat(currentTheme.domains.storefront, " opacity-75")}>(Storefront Crown)</div>
          <div className={"".concat(currentTheme.domains.experimental, " font-bold mt-3")}>
            ⚗️ aistorelab.online
          </div>
          <div className={"".concat(currentTheme.domains.experimental, " opacity-75")}>
            (Experimental Crown)
          </div>
        </div>

        {/* Center Column */}
        <div className="space-y-2">
          <div className={"".concat(currentTheme.domains.personal, " font-bold")}>✍️ jermaineai.com</div>
          <div className={"".concat(currentTheme.domains.personal, " opacity-75")}>(Personal Crown)</div>
          <div className={"".concat(currentTheme.domains.council, " font-bold mt-3")}>
            🏛️ jermaineai.online
          </div>
          <div className={"".concat(currentTheme.domains.council, " opacity-75")}>(Council Crown)</div>
        </div>

        {/* Right Column */}
        <div className="space-y-2">
          <div className={"".concat(currentTheme.domains.educational, " font-bold")}>
            📚 themerrittmethod.com
          </div>
          <div className={"".concat(currentTheme.domains.educational, " opacity-75")}>
            (Educational Crown)
          </div>
          <div className={"".concat(currentTheme.domains.premium, " font-bold mt-3")}>
            💎 jermaineai.store
          </div>
          <div className={"".concat(currentTheme.domains.premium, " opacity-75")}>(Premium Crown)</div>
        </div>
      </div>

      {/* Sacred Inscription */}
      <div className="mt-6 pt-4 border-t border-gray-600">
        <div className="text-yellow-400 text-xs italic">
          "Each crown serves the eternal flame, all bound in sacred constellation"
        </div>
      </div>
    </div>);
};
exports.default = ConstellationAscii;
