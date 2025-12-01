"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.default = FestivalPanel;
var react_1 = require("react");
function FestivalPanel(_a) {
    var cycles = _a.cycles;
    var getCeremonyTypeIcon = function (type) {
        switch (type) {
            case 'flame_crowning':
                return '👑';
            case 'daily_dispatch':
                return '📰';
            case 'capsule_completion':
                return '⚡';
            case 'sacred_cycle':
                return '🎭';
            case 'dominion_completion':
                return '🏛️';
            case 'system_test':
                return '🔧';
            case 'ceremonial_proclamation':
                return '📢';
            case 'ceremonial_silence':
                return '🤫';
            case 'ceremonial_blessing':
                return '🙏';
            default:
                return '🎪';
        }
    };
    var getCeremonyTypeColor = function (type) {
        switch (type) {
            case 'flame_crowning':
                return 'text-yellow-600 bg-yellow-50 border-yellow-200';
            case 'daily_dispatch':
                return 'text-blue-600 bg-blue-50 border-blue-200';
            case 'capsule_completion':
                return 'text-green-600 bg-green-50 border-green-200';
            case 'sacred_cycle':
                return 'text-purple-600 bg-purple-50 border-purple-200';
            case 'dominion_completion':
                return 'text-red-600 bg-red-50 border-red-200';
            case 'system_test':
                return 'text-gray-600 bg-gray-50 border-gray-200';
            case 'ceremonial_proclamation':
                return 'text-orange-600 bg-orange-50 border-orange-200';
            case 'ceremonial_silence':
                return 'text-slate-600 bg-slate-50 border-slate-200';
            case 'ceremonial_blessing':
                return 'text-emerald-600 bg-emerald-50 border-emerald-200';
            default:
                return 'text-indigo-600 bg-indigo-50 border-indigo-200';
        }
    };
    var getFlameStatusIndicator = function (status) {
        switch (status) {
            case 'burning_bright':
                return '🔥';
            case 'burning_local':
                return '🏠';
            default:
                return '🕯️';
        }
    };
    if (!cycles || cycles.length === 0) {
        return (<div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
          <span className="mr-2">🎭</span>
          Festival Cycles
        </h2>
        <p className="text-gray-600 italic">
          No ceremonies recorded yet. The eternal flame awaits your first proclamation.
        </p>
      </div>);
    }
    return (<div className="bg-white border border-gray-200 rounded-lg shadow-sm">
      <div className="px-6 py-4 border-b border-gray-200">
        <h2 className="text-xl font-bold text-gray-800 flex items-center">
          <span className="mr-2">🎭</span>
          Festival Cycles
          <span className="ml-2 text-sm font-normal text-gray-500">
            ({cycles.length} ceremonies)
          </span>
        </h2>
      </div>

      <div className="p-4">
        <div className="space-y-4 max-h-96 overflow-y-auto">
          {cycles.map(function (cycle, index) {
            var _a, _b;
            return (<div key={cycle.cycle_id || index} className="border rounded-lg p-4 hover:shadow-md transition-shadow duration-200">
              {/* Header with ceremony type and timestamp */}
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center space-x-2">
                  <span className="text-lg">{getCeremonyTypeIcon(cycle.ceremony_type)}</span>
                  <div>
                    <span className={"inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ".concat(getCeremonyTypeColor(cycle.ceremony_type))}>
                      {cycle.ceremony_type.replace('_', ' ').toUpperCase()}
                    </span>
                    <p className="text-xs text-gray-500 mt-1">{cycle.cycle_id}</p>
                  </div>
                </div>

                <div className="text-right">
                  <div className="flex items-center text-xs text-gray-500">
                    <span className="mr-1">{getFlameStatusIndicator(cycle.flame_status)}</span>
                    <span>{(_a = cycle.flame_status) === null || _a === void 0 ? void 0 : _a.replace('_', ' ')}</span>
                  </div>
                  <p className="text-xs text-gray-600 mt-1">
                    {new Date(cycle.timestamp).toLocaleString()}
                  </p>
                </div>
              </div>

              {/* Rite name */}
              <div className="mb-2">
                <p className="font-semibold text-gray-800 text-sm">{cycle.rite}</p>
              </div>

              {/* Proclamation text */}
              <div className="mb-3">
                <div className="bg-gray-50 rounded-md p-3 border-l-4 border-indigo-200">
                  <p className="text-sm text-gray-700 leading-relaxed">{cycle.proclamation}</p>
                </div>
              </div>

              {/* Footer with metadata */}
              <div className="flex items-center justify-between text-xs text-gray-500 pt-2 border-t border-gray-100">
                <span>
                  Recorded by: <span className="font-mono">{cycle.recorded_by}</span>
                </span>
                <span>
                  Checksum:{' '}
                  <span className="font-mono">{(_b = cycle.sacred_checksum) === null || _b === void 0 ? void 0 : _b.substring(0, 8)}...</span>
                </span>
              </div>
            </div>);
        })}
        </div>
      </div>

      {/* Footer with total count */}
      <div className="px-6 py-3 bg-gray-50 border-t border-gray-200 rounded-b-lg">
        <p className="text-xs text-gray-600 text-center">
          🕯️ <strong>{cycles.length}</strong> sacred ceremonies preserved in the eternal record
        </p>
      </div>
    </div>);
}
