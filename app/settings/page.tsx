import RunLevelSelector from './components/RunLevelSelector'
import SystemIdentity from './components/SystemIdentity'

export default function SettingsPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-serif text-ceremonial mb-2">
          ⚙️ System Settings
        </h1>
        <p className="text-proclamation">
          Configuration, Identity & System Control
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="codex-card">
            <h2 className="text-2xl font-serif text-codex-gold mb-6">
              General Settings
            </h2>

            <div className="space-y-4">
              <div>
                <label className="text-sm text-codex-parchment/70 block mb-2">System Name</label>
                <input
                  type="text"
                  defaultValue="Codex Dominion"
                  className="w-full bg-codex-navy/50 border border-codex-gold/30 rounded px-4 py-2 text-codex-parchment"
                />
              </div>

              <div>
                <label className="text-sm text-codex-parchment/70 block mb-2">Environment</label>
                <select className="w-full bg-codex-navy/50 border border-codex-gold/30 rounded px-4 py-2 text-codex-parchment">
                  <option>Production</option>
                  <option>Staging</option>
                  <option>Development</option>
                </select>
              </div>

              <div>
                <label className="text-sm text-codex-parchment/70 block mb-2">Time Zone</label>
                <select className="w-full bg-codex-navy/50 border border-codex-gold/30 rounded px-4 py-2 text-codex-parchment">
                  <option>UTC</option>
                  <option>America/New_York</option>
                  <option>Europe/London</option>
                </select>
              </div>
            </div>

            <div className="mt-6 pt-6 border-t border-codex-gold/20">
              <button className="codex-button mr-2">💾 Save Changes</button>
              <button className="codex-button">↩️ Reset Defaults</button>
            </div>
          </div>

          <RunLevelSelector />
        </div>

        <div>
          <SystemIdentity />
        </div>
      </div>
    </div>
  )
}
