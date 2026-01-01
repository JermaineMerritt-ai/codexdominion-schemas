import React from 'react';

interface HomeLayoutProps {
  header: React.ReactNode;
  leftColumn: React.ReactNode;
  rightColumn: React.ReactNode;
}

export default function HomeLayout({ header, leftColumn, rightColumn }: HomeLayoutProps) {
  return (
    <div className="min-h-screen bg-gray-100">
      {/* Top Bar */}
      {header}

      {/* Main Content: 2-column layout */}
      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column (Civilization Pulse) - 2/3 width */}
          <div className="lg:col-span-2 space-y-6">
            {leftColumn}
          </div>

          {/* Right Column (My Circle + Progress or Admin) - 1/3 width */}
          <div className="lg:col-span-1 space-y-6">
            {rightColumn}
          </div>
        </div>
      </div>
    </div>
  );
}
